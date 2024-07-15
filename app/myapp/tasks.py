# tasks.py
import os
import subprocess
import shutil
import logging
import psutil
import time
from PIL import ImageOps, Image
from celery import shared_task
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
from .ready_video_move import move_video


logger = logging.getLogger(__name__)


def convert_to_jpg(image_path):
    with Image.open(image_path) as img:
        # Save the image as a JPEG
        jpg_path = os.path.splitext(image_path)[0] + '.jpg'
        img.convert('RGB').save(jpg_path, 'JPEG')
        return jpg_path


def is_blender_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'blender.exe':
            return True
    return False


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if out:
        logger.info(out.decode('utf-8'))
    if err:
        logger.error(err.decode('utf-8'))


def run_blender_command(template):
    os.chdir(settings.BASE_DIR)

    OPEN_RENDER_PATH = os.path.join(
        settings.BASE_DIR, 'myapp', 'open_and_render.py')



    command = f'{settings.BLENDER_PATH} -P {OPEN_RENDER_PATH} -- "{settings.BASE_DIR}\\{template}"'
    run_command(command)


def remove_bg_and_wait(image_path):
    # Background removing process
    image_name = os.path.basename(image_path)
    bgrem_path = os.path.join(settings.MEDIA_ROOT, 'bgrem', image_name)
    command = f'backgroundremover -i "{image_path}" -m "u2net_human_seg" -a -ae 10  -o "{bgrem_path}"'
    # command = f'backgroundremover -i "{image_path}" -m "u2netp" -a -ae 15  -o "{bgrem_path}"'
    # command = f'backgroundremover -i "{image_path}" -m "u2net_human_seg" -o "{bgrem_path}"'
    process = subprocess.Popen(command, shell=True)
    process.wait()


def rembg_and_wait(image_path):
    # Background removing process
    model_name = settings.MODEL_NAME
    image_name = os.path.basename(image_path)
    model_path = os.path.join(settings.REMBG_PATH, 'models', model_name)
    run_file_path = os.path.join(settings.REMBG_PATH, 'run_console.py')
    bgrem_path = os.path.join(settings.MEDIA_ROOT, 'bgrem', image_name)
    command = f'python "{run_file_path}" "{image_path}" "{bgrem_path}" "{model_path}"'
    process = subprocess.Popen(command, shell=True)
    process.wait()
    # Wait for the BgRem droplet to finish
    while not os.path.exists(bgrem_path):
        logging.info(
            f'Waiting for {image_name} to be processed by the bgrem...')
        time.sleep(1)  # Wait for 1 second before checking again
    logging.info(f'{image_name} has been processed by rembg.')


def alpha_transparency_contrast(img):
    threshold_low = settings.THRESHOLD_LOW
    threshold_high = settings.THRESHOLD_HIGH
    data = img.getdata()
    new_data = []

    for item in data:
        alpha = item[3]

        # If alpha is less than or equal to threshold_low, make the pixel fully transparent
        if alpha <= threshold_low:
            new_alpha = 0
        # If alpha is greater than or equal to threshold_high, make the pixel not transparent
        elif alpha >= threshold_high:
            new_alpha = 255
        # For alpha values between threshold_low and threshold_high, adjust using linear interpolation
        else:
            new_alpha = int((alpha - threshold_low) * 255 /
                            (threshold_high - threshold_low))
        new_data.append((item[0], item[1], item[2], new_alpha))

    img.putdata(new_data)

    return img


def prepare_image(image_path, new_name, new_dir):
    os.makedirs(new_dir, exist_ok=True)

    with Image.open(image_path) as img:
        # Ensure the image has an alpha channel
        img = img.convert("RGBA")

        # Apply the function to convert semi-transparent pixels
        alpha_transparency_contrast(img)

        # Get the bounding box
        bbox = img.getbbox()

        # If there's no bounding box, the image is fully transparent
        if not bbox:
            logger.info(f'Image at {image_path} is fully transparent.')
            return None

        # Crop the image to the bounding box
        cropped_img = img.crop(bbox)

        max_size = max(cropped_img.size)
        new_image = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0))
        new_image.paste(cropped_img, ((
            max_size - cropped_img.size[0])//2, (max_size - cropped_img.size[1])//2))

        new_image = ImageOps.expand(new_image, border=5, fill=(0, 0, 0, 0))
        new_path = os.path.join(new_dir, new_name)
        new_image.save(new_path, 'PNG')
        logger.info(f'Saved and moved image to: {new_path}')

    os.remove(image_path)
    logger.info(f'Deleted original image at: {image_path}')
    return new_path


@shared_task
def process_images_and_render_video(image1_name, image2_name, email, template):
    try:
        image1_path = os.path.join(
            settings.MEDIA_ROOT, image1_name).replace('/', '\\')
        image2_path = os.path.join(
            settings.MEDIA_ROOT, image2_name).replace('/', '\\')
        logger.info(
            f'Image 1 path: {image1_path}, Image 2 path: {image2_path}')

        # Call the function for both images
        rembg_and_wait(image1_path)
        rembg_and_wait(image2_path)

        image1_name = os.path.basename(image1_name)
        image2_name = os.path.basename(image2_name)

        image1_path = os.path.join(settings.MEDIA_ROOT, 'bgrem', image1_name)
        image2_path = os.path.join(settings.MEDIA_ROOT, 'bgrem', image2_name)

        while is_blender_running():
            time.sleep(10)

        image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        image1_new_name = "portrait_0.png"
        image2_new_name = "portrait_1.png"

        image_in_use_path1 = prepare_image(
            image1_path, image1_new_name, image_in_use_dir)
        image_in_use_path2 = prepare_image(
            image2_path, image2_new_name, image_in_use_dir)

        # template = r"templates_BBS\template_blend\port_port.blend"
        logger.info('Start Blender...')
        run_blender_command(template)

        logger.info('Clean up images_in_use...')
        os.remove(image_in_use_path1)
        os.remove(image_in_use_path2)

        while is_blender_running():
            time.sleep(5)

        input_folder = os.path.join(
            settings.BASE_DIR, 'media', settings.BLENDER_OUTPUT)
        output_folder = os.path.join(settings.BASE_DIR, 'media', 'ready')

        new_filename = move_video(input_folder, output_folder, email)
        video_path = os.path.join(output_folder, new_filename)

        # attach video file to the email
        message = f'Your video is ready! It is attached to this email.'
        email = EmailMessage('Your video is ready', message,
                             'noreply@yourwebsite.com', [email])
        # Reading video file in binary mode
        with open(video_path, 'rb') as video_file:
            email.attach(new_filename, video_file.read(),
                         'application/octet-stream')
        email.send(fail_silently=False)

        # Sending Link to the video
        # video_link = f"http://130.204.72.204:8000/media/ready/{new_filename}"
        # message = f'Your video is ready! You can watch it here: {video_link}'
        # send_mail('Your video is ready', message, 'noreply@yourwebsite.com', [email], fail_silently=False)

    except Exception as e:
        logger.error(f"Error in process_images_and_render_video: {e}")
