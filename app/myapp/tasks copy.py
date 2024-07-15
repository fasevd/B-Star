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

# BLENDER_PATH = r"E:\Projects\Python\Ivan\blender-3.2.2\blender.exe"
# settings.BASE_DIR = r"E:\Projects\Python\Ivan\billboardstar_2\app"
# PHOTOSHOP_DROPLET_PATH = os.path.join(settings.BASE_DIR, 'myapp', 'BS_Droplet.exe')
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

    OPEN_RENDER_PATH = os.path.join(settings.BASE_DIR, 'myapp', 'open_and_render.py') 

    command = f'{settings.BLENDER_PATH} -P {OPEN_RENDER_PATH} -- "{settings.BASE_DIR}\\{template}"'
    run_command(command)

def run_photoshop_droplet(image_path):
    command = [settings.PHOTOSHOP_DROPLET_PATH, image_path]
    run_command(command)

def prepare_image(image_path, new_name, new_dir):
    os.makedirs(new_dir, exist_ok=True)
    with Image.open(image_path) as image:
        max_size = max(image.size)
        new_image = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0)) 
        new_image.paste(image, ((max_size - image.size[0])//2, (max_size - image.size[1])//2))
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
        image1_path = os.path.join(settings.MEDIA_ROOT, image1_name).replace('/', '\\')
        image2_path = os.path.join(settings.MEDIA_ROOT, image2_name).replace('/', '\\')
        logger.info(f'Image 1 path: {image1_path}, Image 2 path: {image2_path}')

        # Convert the images to JPEG format
        image1_path_jpg = convert_to_jpg(image1_path)
        image2_path_jpg = convert_to_jpg(image2_path)
        
        run_photoshop_droplet(image1_path_jpg)
        run_photoshop_droplet(image2_path_jpg)

        image1_name = os.path.basename(image1_name)
        image2_name = os.path.basename(image2_name)

        image1_path = os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image1_name)
        image2_path = os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image2_name)

        while is_blender_running():
            time.sleep(10)

        image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        image1_new_name = "portrait_0.png"
        image2_new_name = "portrait_1.png"

        image_in_use_path1 = prepare_image(image1_path, image1_new_name, image_in_use_dir)
        image_in_use_path2 = prepare_image(image2_path, image2_new_name, image_in_use_dir)

        # template = r"templates_BBS\template_blend\port_port.blend"
        logger.info('Start Blender...')
        run_blender_command(template)

        logger.info('Clean up images_in_use...')
        os.remove(image_in_use_path1)
        os.remove(image_in_use_path2)

        while is_blender_running():
            time.sleep(5)
        
        input_folder = os.path.join(settings.BASE_DIR, 'media', 'blender_output')
        output_folder = os.path.join(settings.BASE_DIR, 'media', 'ready')

        new_filename = move_video(input_folder, output_folder, email)
        video_path = os.path.join(output_folder, new_filename)

        #attach video file to the email
        message = f'Your video is ready! It is attached to this email.'
        email = EmailMessage('Your video is ready', message, 'noreply@yourwebsite.com', [email])
        # Reading video file in binary mode
        with open(video_path, 'rb') as video_file:
            email.attach(new_filename, video_file.read(), 'application/octet-stream')
        email.send(fail_silently=False)

        #Sending Link to the video
        # video_link = f"http://130.204.72.204:8000/media/ready/{new_filename}"
        # message = f'Your video is ready! You can watch it here: {video_link}'
        # send_mail('Your video is ready', message, 'noreply@yourwebsite.com', [email], fail_silently=False)

    except Exception as e:
        logger.error(f"Error in process_images_and_render_video: {e}")


































import os
import subprocess
import shutil
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging
import psutil
import time
from PIL import ImageOps
from PIL import Image
from .move_ready_video_2 import move_video


logger = logging.getLogger(__name__)

def is_blender_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'blender.exe':
            return True
    return False

def run_blender_command(template):
    # Set your working directory
    os.chdir('C:\\B-Star\\billboardstar_2\\app')
    
    # Define your command
    command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\' + template + '"'

    # # Define your command
    # command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\templates_BBS\\template_blend\\port_port.blend"'

    # Run your command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    # Optionally print stdout and stderr
    out, err = process.communicate()
    print(f"stdout: {out.decode('utf-8')}")
    if err:
        print(f"stderr: {err.decode('utf-8')}")


# def get_image_ratio(image_path):
#     image = Image.open(image_path)
#     image = ImageOps.exif_transpose(image)  # consider EXIF data

#     width, height = image.size
#     if width > height:
#         # return "landscape"
#         return "portrait"
#     elif width < height:
#         return "portrait"
#     else:
#         # return "square"
#         return "portrait"


# def get_new_path(image_dir, image_name):
#     base_name, ext = os.path.splitext(image_name)
#     counter = 0
#     while True:
#         new_name = f"{base_name}_{counter}{ext}"
#         new_path = os.path.join(image_dir, new_name)
#         if not os.path.exists(new_path):
#             return new_path
#         counter += 1

@shared_task
def process_images_and_render_video(image1_name, image2_name, email):


    # Get the full paths to the files
    logging.info('Getting image paths...')
    image1_path = os.path.join(settings.MEDIA_ROOT, image1_name).replace('/', '\\')
    image2_path = os.path.join(settings.MEDIA_ROOT, image2_name).replace('/', '\\')
    
    logging.info(f'Image 1 path: {image1_path}')
    logging.info(f'Image 2 path: {image2_path}')

    # Run the Photoshop droplet
    logging.info('Running Photoshop droplet...')
    subprocess.run([r"E:\Projects\Python\Ivan\billboardstar_2\app\myapp\BS_Droplet.exe", image1_path])
    subprocess.run([r"E:\Projects\Python\Ivan\billboardstar_2\app\myapp\BS_Droplet.exe", image2_path])

    image1_name = os.path.basename(image1_name)
    image2_name = os.path.basename(image2_name)
    # Paths to the droplet-processed files
    image1_path = os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image1_name)
    image2_path = os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image2_name)


        # Wait for any running Blender processes to finish
    while is_blender_running():
        time.sleep(10)  # Wait for 10 seconds before checking again

        # Move and convert the images into png, also renaming "portrait.png", "landscape.png" and "square.png" 
    try:
        # Full paths to the files
        logging.info('Getting image paths...')
        logging.info(f'Image 1 path: {image1_path}')
        logging.info(f'Image 2 path: {image2_path}')

        image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        os.makedirs(image_in_use_dir, exist_ok=True)

        logging.info(f'Images will be moved to: {image_in_use_dir}')

        # New names for the images
        image1_new_name = "portrait_0.png"
        image2_new_name = "portrait_1.png"

        logging.info(f'Image 1 will be renamed to: {image1_new_name}')
        logging.info(f'Image 2 will be renamed to: {image2_new_name}')

        image_in_use_path1 = os.path.join(image_in_use_dir, image1_new_name)


        logging.info('Moving and converting image 1...')
        with Image.open(image1_path) as image1:
            max_size = max(image1.size)
            new_image1 = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0))  # create a new image with the maximum dimension and transparent background
            new_image1.paste(image1, ((max_size - image1.size[0])//2, (max_size - image1.size[1])//2))  # paste the original image into the center of the new image
            new_image1 = ImageOps.expand(new_image1, border=5, fill=(0, 0, 0, 0))  # add 5 extra transparent pixels on each side
            new_image1.save(image_in_use_path1, 'PNG')  
            logging.info(f'Saved and moved image 1 to: {image_in_use_path1}')

        image_in_use_path2 = os.path.join(image_in_use_dir, image2_new_name)

        logging.info('Moving and converting image 2...')
        with Image.open(image2_path) as image2:
            max_size = max(image2.size)
            new_image2 = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0))  # create a new image with the maximum dimension and transparent background
            new_image2.paste(image2, ((max_size - image2.size[0])//2, (max_size - image2.size[1])//2))  # paste the original image into the center of the new image
            new_image2 = ImageOps.expand(new_image2, border=5, fill=(0, 0, 0, 0))  # add 5 extra transparent pixels on each side
            new_image2.save(image_in_use_path2, 'PNG') 
            logging.info(f'Saved and moved image 2 to: {image_in_use_path2}')

        # Remove the original images
        os.remove(image1_path)
        os.remove(image2_path)

        logging.info(f'Deleted original image 1 at: {image1_path}')
        logging.info(f'Deleted original image 2 at: {image2_path}')


        # logging.info('Moving and converting image 1...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGBA').save(image_in_use_path1, 'PNG')  
        #     logging.info(f'Saved and moved image 1 to: {image_in_use_path1}')

        # image_in_use_path2 = os.path.join(image_in_use_dir, image2_new_name)

        # logging.info('Moving and converting image 2...')
        # with Image.open(image2_path) as image2:
        #     image2.convert('RGBA').save(image_in_use_path2, 'PNG') 
        #     logging.info(f'Saved and moved image 2 to: {image_in_use_path2}')

        # # Remove the original images
        # os.remove(image1_path)
        # os.remove(image2_path)

        # logging.info(f'Deleted original image 1 at: {image1_path}')
        # logging.info(f'Deleted original image 2 at: {image2_path}')

        template = r"templates_BBS\template_blend\port_port.blend"


        # Start Blender
        logger.info('Start Blender...')



        run_blender_command(template)

        # Cleanup: Delete the images in image_in_use
        logger.info('Clen Up images_in_use...')
        os.remove(image_in_use_path1)
        os.remove(image_in_use_path2)

        while is_blender_running():
            time.sleep(5)  # Wait for 10 seconds before checking again
        # move video and send email and message
        input_folder = r"E:\Projects\Python\Ivan\billboardstar_2\app\media\blender_output"
        output_folder = r"E:\Projects\Python\Ivan\billboardstar_2\app\media\ready"

        new_filename = move_video(input_folder, output_folder, email)

        
        #BLUE - Send the email with a link to the video
        video_link = "http://130.204.72.204:8000/media/ready/" + new_filename  # Construct the URL to the video
        # video_link = "http://yourwebsite.com/videos/" + email + ".mp4"  # Construct the URL to the video
        message = f"Your video is ready! You can watch it here: {video_link}"
        send_mail(
            'Your video is ready',
            message,
            'noreply@yourwebsite.com',
            [email],
            fail_silently=False,
        )

    except Exception as e:
        logging.error(f"Error in process_images_and_render_video: {e}")





#Checks the image ratio and chose blender template
@shared_task
def process_images_and_render_video(image1_name, image2_name, email):


    # Get the full paths to the files
    logging.info('Getting image paths...')
    image1_path = os.path.join(settings.MEDIA_ROOT, image1_name).replace('/', '\\')
    image2_path = os.path.join(settings.MEDIA_ROOT, image2_name).replace('/', '\\')
    
    logging.info(f'Image 1 path: {image1_path}')
    logging.info(f'Image 2 path: {image2_path}')

    # Run the Photoshop droplet
    logging.info('Running Photoshop droplet...')
    subprocess.run([r"E:\Projects\Python\Ivan\billboardstar_2\app\myapp\BS_Droplet.exe", image1_path])
    subprocess.run([r"E:\Projects\Python\Ivan\billboardstar_2\app\myapp\BS_Droplet.exe", image2_path])


    # # Get the base name and extension
    # image1_base, image1_ext = os.path.splitext(image1_name)
    # image2_base, image2_ext = os.path.splitext(image2_name)

    # # Update the extension to .png
    # image1_name = f"{image1_base}.png"
    # image2_name = f"{image2_base}.png"




    # # Wait for the Photoshop droplet to finish
    # while not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image1_name)):
    #     logging.info(f'Waiting for image 1 to be processed by the droplet...')
    #     time.sleep(1)  # Wait for 1 seconds before checking again
    # logging.info('Image 1 has been processed by the droplet.')

    # while not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image2_name)):
    #     logging.info(f'Waiting for image 2 to be processed by the droplet...')
    #     time.sleep(1)  # Wait for 1 seconds before checking again
    # logging.info('Image 2 has been processed by the droplet.')

    image1_name = os.path.basename(image1_name)
    image2_name = os.path.basename(image2_name)
    # Paths to the droplet-processed files
    image1_path = os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image1_name)
    image2_path = os.path.join(settings.MEDIA_ROOT, 'droplet_ready', image2_name)


        # Wait for any running Blender processes to finish
    while is_blender_running():
        time.sleep(10)  # Wait for 10 seconds before checking again

        # Move and convert the images into png, also renaming "portrait.png", "landscape.png" and "square.png" 
    try:
        # Full paths to the files
        logging.info('Getting image paths...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        logging.info(f'Image 1 path: {image1_path}')
        logging.info(f'Image 2 path: {image2_path}')

        image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        os.makedirs(image_in_use_dir, exist_ok=True)

        logging.info(f'Images will be moved to: {image_in_use_dir}')

        # Determine the ratio and set new names accordingly
        logging.info('Getting image ratios...')
        image1_ratio = get_image_ratio(image1_path)
        image2_ratio = get_image_ratio(image2_path)

        image1_new_name = image1_ratio + '.png'
        image2_new_name = image2_ratio + '.png'

        logging.info(f'Image 1 ratio: {image1_ratio}')
        logging.info(f'Image 2 ratio: {image2_ratio}')

        # Determine the template
        if image1_ratio == image2_ratio == "landscape":
            template = r"templates_BBS\template_blend\land_land.blend"
        elif image1_ratio == image2_ratio == "portrait":
            template = r"templates_BBS\template_blend\port_port.blend"
        else:
            template = r"templates_BBS\template_blend\land_port.blend"

        logging.info(f'Template: {template}')

        image_in_use_path1 = get_new_path(image_in_use_dir, image1_new_name)

        logging.info('Moving and converting image 1...')
        with Image.open(image1_path) as image1:
            image1.convert('RGBA').save(image_in_use_path1, 'PNG')  
            logging.info(f'Saved and moved image 1 to: {image_in_use_path1}')

        image_in_use_path2 = get_new_path(image_in_use_dir, image2_new_name)

        logging.info('Moving and converting image 2...')
        with Image.open(image2_path) as image2:
            image2.convert('RGBA').save(image_in_use_path2, 'PNG') 
            logging.info(f'Saved and moved image 2 to: {image_in_use_path2}')

        # Remove the original images
        os.remove(image1_path)
        os.remove(image2_path)

        logging.info(f'Deleted original image 1 at: {image1_path}')
        logging.info(f'Deleted original image 2 at: {image2_path}')


        # # Full paths to the files
        # logging.info('Getting image paths...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        # logging.info(f'Image 1 path: {image1_path}')
        # logging.info(f'Image 2 path: {image2_path}')

        # image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        # os.makedirs(image_in_use_dir, exist_ok=True)

        # logging.info(f'Images will be moved to: {image_in_use_dir}')

        # # Determine the ratio and set new names accordingly
        # logging.info('Getting image ratios...')
        # image1_new_name = get_image_ratio(image1_path) + '.png'
        # image2_new_name = get_image_ratio(image2_path) + '.png'

        # logging.info(f'Image 1 ratio: {image1_new_name}')
        # logging.info(f'Image 2 ratio: {image2_new_name}')

        # image_in_use_path1 = get_new_path(image_in_use_dir, image1_new_name)

        # logging.info('Moving and converting image 1...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGB').save(image_in_use_path1, 'PNG')  
        #     logging.info(f'Saved and moved image 1 to: {image_in_use_path1}')

        # image_in_use_path2 = get_new_path(image_in_use_dir, image2_new_name)

        # logging.info('Moving and converting image 2...')
        # with Image.open(image2_path) as image2:
        #     image2.convert('RGB').save(image_in_use_path2, 'PNG') 
        #     logging.info(f'Saved and moved image 2 to: {image_in_use_path2}')

        # # Remove the original images
        # os.remove(image1_path)
        # os.remove(image2_path)

        # logging.info(f'Deleted original image 1 at: {image1_path}')
        # logging.info(f'Deleted original image 2 at: {image2_path}')
        # # Full paths to the files
        # logger.info('Pathing images...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        # image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        # os.makedirs(image_in_use_dir, exist_ok=True)

        # # Determine the ratio and set new names accordingly
        # image1_new_name = get_image_ratio(image1_path) + '.png'
        # image2_new_name = get_image_ratio(image2_path) + '.png'

        # image_in_use_path1 = get_new_path(image_in_use_dir, image1_new_name)
        # image_in_use_path2 = get_new_path(image_in_use_dir, image2_new_name)

        # logger.info('Moving and converting images...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGB').save(image_in_use_path1, 'PNG')  

        # with Image.open(image2_path) as image2:
        #     image2.convert('RGB').save(image_in_use_path2, 'PNG') 

        # # Remove the original images
        # os.remove(image1_path)
        # os.remove(image2_path)
        # # Full paths to the files
        # logger.info('Pathing images...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        # image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        # os.makedirs(image_in_use_dir, exist_ok=True)

        # # Determine the ratio and set new names accordingly
        # image1_new_name = get_image_ratio(image1_path) + '.png'
        # image2_new_name = get_image_ratio(image2_path) + '.png'

        # image_in_use_path1 = os.path.join(image_in_use_dir, image1_new_name)
        # image_in_use_path2 = os.path.join(image_in_use_dir, image2_new_name)

        # logger.info('Moving and converting images...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGB').save(image_in_use_path1, 'PNG')  
        # shutil.move(image1_path, image_in_use_path1)

        # with Image.open(image2_path) as image2:
        #     image2.convert('RGB').save(image_in_use_path2, 'PNG') 
        # shutil.move(image2_path, image_in_use_path2)

        # Start Blender
        logger.info('Start Blender...')

        def run_blender_command():
            # Set your working directory
            os.chdir('C:\\B-Star\\billboardstar_2\\app')
            
            # Define your command
            command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\' + template + '"'

            # # Define your command
            # command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\tsq1.blend"'

            # Run your command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            
            # Optionally print stdout and stderr
            out, err = process.communicate()
            print(f"stdout: {out.decode('utf-8')}")
            if err:
                print(f"stderr: {err.decode('utf-8')}")

        run_blender_command()

        # Cleanup: Delete the images in image_in_use
        logger.info('Clen Up images_in_use...')
        os.remove(image_in_use_path1)
        os.remove(image_in_use_path2)

        while is_blender_running():
            time.sleep(5)  # Wait for 10 seconds before checking again
        # move video and send email and message
        input_folder = r"E:\Projects\Python\Ivan\billboardstar_2\app\media\blender_output"
        output_folder = r"E:\Projects\Python\Ivan\billboardstar_2\app\media\ready"
        # input_folder = r"E:\Projects\Python\Ivan\billboardstar_2\test\input"
        # output_folder = r"E:\Projects\Python\Ivan\billboardstar_2\test\output"
        new_filename = move_video(input_folder, output_folder, email)

        
        #BLUE - Send the email with a link to the video
        video_link = "http://130.204.72.204:8000/media/ready/" + new_filename  # Construct the URL to the video
        # video_link = "http://yourwebsite.com/videos/" + email + ".mp4"  # Construct the URL to the video
        message = f"Your video is ready! You can watch it here: {video_link}"
        send_mail(
            'Your video is ready',
            message,
            'noreply@yourwebsite.com',
            [email],
            fail_silently=False,
        )

    except Exception as e:
        logging.error(f"Error in process_images_and_render_video: {e}")









@shared_task
def process_images_and_render_video(image1_name, image2_name, email):
        # Wait for any running Blender processes to finish
    while is_blender_running():
        time.sleep(10)  # Wait for 10 seconds before checking again

        # Move and convert the images into png, also renaming "portrait.png", "landscape.png" and "square.png" 
    try:
        # Full paths to the files
        logging.info('Getting image paths...')
        image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        logging.info(f'Image 1 path: {image1_path}')
        logging.info(f'Image 2 path: {image2_path}')

        image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        os.makedirs(image_in_use_dir, exist_ok=True)

        logging.info(f'Images will be moved to: {image_in_use_dir}')

        # Determine the ratio and set new names accordingly
        logging.info('Getting image ratios...')
        image1_ratio = get_image_ratio(image1_path)
        image2_ratio = get_image_ratio(image2_path)

        image1_new_name = image1_ratio + '.png'
        image2_new_name = image2_ratio + '.png'

        logging.info(f'Image 1 ratio: {image1_ratio}')
        logging.info(f'Image 2 ratio: {image2_ratio}')

        # Determine the template
        if image1_ratio == image2_ratio == "landscape":
            template = r"templates_BBS\template_blend\land_land.blend"
        elif image1_ratio == image2_ratio == "portrait":
            template = r"templates_BBS\template_blend\port_port.blend"
        else:
            template = r"templates_BBS\template_blend\land_port.blend"

        logging.info(f'Template: {template}')

        image_in_use_path1 = get_new_path(image_in_use_dir, image1_new_name)

        logging.info('Moving and converting image 1...')
        with Image.open(image1_path) as image1:
            image1.convert('RGBA').save(image_in_use_path1, 'PNG')  
            logging.info(f'Saved and moved image 1 to: {image_in_use_path1}')

        image_in_use_path2 = get_new_path(image_in_use_dir, image2_new_name)

        logging.info('Moving and converting image 2...')
        with Image.open(image2_path) as image2:
            image2.convert('RGBA').save(image_in_use_path2, 'PNG') 
            logging.info(f'Saved and moved image 2 to: {image_in_use_path2}')

        # Remove the original images
        os.remove(image1_path)
        os.remove(image2_path)

        logging.info(f'Deleted original image 1 at: {image1_path}')
        logging.info(f'Deleted original image 2 at: {image2_path}')


        # # Full paths to the files
        # logging.info('Getting image paths...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        # logging.info(f'Image 1 path: {image1_path}')
        # logging.info(f'Image 2 path: {image2_path}')

        # image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        # os.makedirs(image_in_use_dir, exist_ok=True)

        # logging.info(f'Images will be moved to: {image_in_use_dir}')

        # # Determine the ratio and set new names accordingly
        # logging.info('Getting image ratios...')
        # image1_new_name = get_image_ratio(image1_path) + '.png'
        # image2_new_name = get_image_ratio(image2_path) + '.png'

        # logging.info(f'Image 1 ratio: {image1_new_name}')
        # logging.info(f'Image 2 ratio: {image2_new_name}')

        # image_in_use_path1 = get_new_path(image_in_use_dir, image1_new_name)

        # logging.info('Moving and converting image 1...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGB').save(image_in_use_path1, 'PNG')  
        #     logging.info(f'Saved and moved image 1 to: {image_in_use_path1}')

        # image_in_use_path2 = get_new_path(image_in_use_dir, image2_new_name)

        # logging.info('Moving and converting image 2...')
        # with Image.open(image2_path) as image2:
        #     image2.convert('RGB').save(image_in_use_path2, 'PNG') 
        #     logging.info(f'Saved and moved image 2 to: {image_in_use_path2}')

        # # Remove the original images
        # os.remove(image1_path)
        # os.remove(image2_path)

        # logging.info(f'Deleted original image 1 at: {image1_path}')
        # logging.info(f'Deleted original image 2 at: {image2_path}')
        # # Full paths to the files
        # logger.info('Pathing images...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        # image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        # os.makedirs(image_in_use_dir, exist_ok=True)

        # # Determine the ratio and set new names accordingly
        # image1_new_name = get_image_ratio(image1_path) + '.png'
        # image2_new_name = get_image_ratio(image2_path) + '.png'

        # image_in_use_path1 = get_new_path(image_in_use_dir, image1_new_name)
        # image_in_use_path2 = get_new_path(image_in_use_dir, image2_new_name)

        # logger.info('Moving and converting images...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGB').save(image_in_use_path1, 'PNG')  

        # with Image.open(image2_path) as image2:
        #     image2.convert('RGB').save(image_in_use_path2, 'PNG') 

        # # Remove the original images
        # os.remove(image1_path)
        # os.remove(image2_path)
        # # Full paths to the files
        # logger.info('Pathing images...')
        # image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        # image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)

        # image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        # os.makedirs(image_in_use_dir, exist_ok=True)

        # # Determine the ratio and set new names accordingly
        # image1_new_name = get_image_ratio(image1_path) + '.png'
        # image2_new_name = get_image_ratio(image2_path) + '.png'

        # image_in_use_path1 = os.path.join(image_in_use_dir, image1_new_name)
        # image_in_use_path2 = os.path.join(image_in_use_dir, image2_new_name)

        # logger.info('Moving and converting images...')
        # with Image.open(image1_path) as image1:
        #     image1.convert('RGB').save(image_in_use_path1, 'PNG')  
        # shutil.move(image1_path, image_in_use_path1)

        # with Image.open(image2_path) as image2:
        #     image2.convert('RGB').save(image_in_use_path2, 'PNG') 
        # shutil.move(image2_path, image_in_use_path2)

        # Start Blender
        logger.info('Start Blender...')

        def run_blender_command():
            # Set your working directory
            os.chdir('C:\\B-Star\\billboardstar_2\\app')
            
            # Define your command
            command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\' + template + '"'

            # # Define your command
            # command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\tsq1.blend"'

            # Run your command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            
            # Optionally print stdout and stderr
            out, err = process.communicate()
            print(f"stdout: {out.decode('utf-8')}")
            if err:
                print(f"stderr: {err.decode('utf-8')}")

        run_blender_command()

        # Cleanup: Delete the images in image_in_use
        logger.info('Clen Up images_in_use...')
        os.remove(image_in_use_path1)
        os.remove(image_in_use_path2)

        while is_blender_running():
            time.sleep(5)  # Wait for 10 seconds before checking again
        # move video and send email and message
        input_folder = r"E:\Projects\Python\Ivan\billboardstar_2\app\media\blender_output"
        output_folder = r"E:\Projects\Python\Ivan\billboardstar_2\app\media\ready"
        # input_folder = r"E:\Projects\Python\Ivan\billboardstar_2\test\input"
        # output_folder = r"E:\Projects\Python\Ivan\billboardstar_2\test\output"
        new_filename = move_video(input_folder, output_folder, email)

        
        #BLUE - Send the email with a link to the video
        video_link = "http://130.204.72.204:8000/media/ready/" + new_filename  # Construct the URL to the video
        # video_link = "http://yourwebsite.com/videos/" + email + ".mp4"  # Construct the URL to the video
        message = f"Your video is ready! You can watch it here: {video_link}"
        send_mail(
            'Your video is ready',
            message,
            'noreply@yourwebsite.com',
            [email],
            fail_silently=False,
        )

    except Exception as e:
        logging.error(f"Error in process_images_and_render_video: {e}")

@shared_task
def process_images_and_render_video(image1_name, image2_name, email):
    # Wait for any running Blender processes to finish
    while is_blender_running():
        time.sleep(10)  # Wait for 10 seconds before checking again
    try:
        # Full paths to the files
        logger.info('Pathing images...')
        image1_path = os.path.join(settings.MEDIA_ROOT, image1_name)
        image2_path = os.path.join(settings.MEDIA_ROOT, image2_name)
        image_in_use_dir = os.path.join(settings.MEDIA_ROOT, 'image_in_use')
        os.makedirs(image_in_use_dir, exist_ok=True)

        image_in_use_path1 = os.path.join(image_in_use_dir, image1_name)
        image_in_use_path2 = os.path.join(image_in_use_dir, image2_name)

        # Move the images to the image_in_use directory
        logger.info('Moving images...')
        shutil.move(image1_path, image_in_use_path1)
        shutil.move(image2_path, image_in_use_path2)

        # Start Blender
        logger.info('Start Blender...')
        run_blender_command()

        # Cleanup: Delete the images in image_in_use
        logger.info('Clean Up images_in_use...')
        os.remove(image_in_use_path1)
        os.remove(image_in_use_path2)

        # Send email with download link to the user
        send_mail_with_download_link(email)

    except Exception as e:
        logging.error(f"Error in process_images_and_render_video: {e}")


def run_blender_command():
    # Set your working directory
    os.chdir('C:\\B-Star\\billboardstar_2\\app')

    # Define your command
    command = '"C:\\B-Star\\blender-3.2.2\\blender.exe" -P open_and_render.py -- "C:\\B-Star\\billboardstar_2\\app\\untitled.blend"'

    # Run your command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    # Optionally print stdout and stderr
    out, err = process.communicate()
    print(f"stdout: {out.decode('utf-8')}")
    if err:
        print(f"stderr: {err.decode('utf-8')}")


    # Optionally print stdout and stderr
    out, err = process.communicate()
    print(f"stdout: {out.decode('utf-8')}")
    if err:
        print(f"stderr: {err.decode('utf-8')}")

def send_mail_with_download_link(email):
    # Define your subject and message
    subject = "Your video is ready for download"
    message = "Here is the download link for your video..."

    # Send the email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])