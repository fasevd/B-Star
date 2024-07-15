# models
# work remove backgrounds, skip - opacity ajuster, and trim transparent area and add pixels to make square ratio

# from django.db import models
# from PIL import Image, ImageOps
# from io import BytesIO
# from django.core.files import File
# from rembg import remove, new_session
# from django.core.files.base import ContentFile

# class ImagePair(models.Model):
#     image1 = models.ImageField(upload_to='images/')
#     image2 = models.ImageField(upload_to='images/')
#     email = models.EmailField(default='default@example.com')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         session = new_session()

#         for image_field in [self.image1, self.image2]:
#             img = Image.open(image_field.path)

#             # If the image has exif data, and the orientation is not 1
#             # transpose it according to its exif data
#             if hasattr(img, "_getexif") and img._getexif() is not None:
#                 orientation = img._getexif().get(0x0112)
#                 img = ImageOps.exif_transpose(img)

#             # check which dimension is larger and resize based on that dimension
#             if img.height > 1080 or img.width > 1080:
#                 output_size = (1080, 1080)
#                 img.thumbnail(output_size)
#                 img.save(image_field.path)

#             # Background removal
#             with open(image_field.path, 'rb') as i:
#                 input_img = i.read()
#                 output_img = remove(input_img, session=session)

#             image = Image.open(BytesIO(output_img))

#             # Trim transparent borders
#             image = image.crop(image.getbbox())

#             # Add a transparent border to make the image a square
#             max_size = max(image.size)
#             new_image = Image.new('RGBA', (max_size, max_size), (0, 0, 0, 0))  # create a new image with the maximum dimension and transparent background
#             new_image.paste(image, ((max_size - image.size[0])//2, (max_size - image.size[1])//2))  # paste the original image into the center of the new image

#             # Add 5 extra transparent pixels on each side
#             new_image = ImageOps.expand(new_image, border=5, fill=(0, 0, 0, 0))

#             # Save the new image
#             buffer = BytesIO()
#             new_image.save(buffer, format='PNG')
#             image_field.save(image_field.name, ContentFile(buffer.getvalue()), save=False)

#         super().save(*args, **kwargs)



# # work remove backgrounds, skip - opacity ajuster, and trim transparent area
# from django.db import models
# from PIL import Image, ImageOps
# from io import BytesIO
# from django.core.files import File
# from rembg import remove, new_session
# from django.core.files.base import ContentFile

# class ImagePair(models.Model):
#     image1 = models.ImageField(upload_to='images/')
#     image2 = models.ImageField(upload_to='images/')
#     email = models.EmailField(default='default@example.com')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         session = new_session()

#         for image_field in [self.image1, self.image2]:
#             img = Image.open(image_field.path)

#             # If the image has exif data, and the orientation is not 1
#             # transpose it according to its exif data
#             if hasattr(img, "_getexif") and img._getexif() is not None:
#                 orientation = img._getexif().get(0x0112)
#                 img = ImageOps.exif_transpose(img)

#             # check which dimension is larger and resize based on that dimension
#             if img.height > 1080 or img.width > 1080:
#                 output_size = (1080, 1080)
#                 img.thumbnail(output_size)
#                 img.save(image_field.path)

#             # Background removal
#             with open(image_field.path, 'rb') as i:
#                 input_img = i.read()
#                 output_img = remove(input_img, session=session)

#             image = Image.open(BytesIO(output_img))

#             # Trim transparent borders
#             image = image.crop(image.getbbox())

#             # Save the new image
#             buffer = BytesIO()
#             image.save(buffer, format='PNG')
#             image_field.save(image_field.name, ContentFile(buffer.getvalue()), save=False)

#         super().save(*args, **kwargs)

# # work remove backgrounds, opacity ajuster, and trim transparent area
# from django.db import models
# from PIL import Image, ImageOps
# from io import BytesIO
# from django.core.files import File
# from rembg import remove, new_session
# from django.core.files.base import ContentFile

# class ImagePair(models.Model):
#     image1 = models.ImageField(upload_to='images/')
#     image2 = models.ImageField(upload_to='images/')
#     email = models.EmailField(default='default@example.com')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         session = new_session()

#         for image_field in [self.image1, self.image2]:
#             img = Image.open(image_field.path)

#             # If the image has exif data, and the orientation is not 1
#             # transpose it according to its exif data
#             if hasattr(img, "_getexif") and img._getexif() is not None:
#                 orientation = img._getexif().get(0x0112)
#                 img = ImageOps.exif_transpose(img)

#             # check which dimension is larger and resize based on that dimension
#             if img.height > 1920 or img.width > 1920:
#                 output_size = (1920, 1920)
#                 img.thumbnail(output_size)
#                 img.save(image_field.path)

#             # Background removal
#             with open(image_field.path, 'rb') as i:
#                 input_img = i.read()
#                 output_img = remove(input_img, session=session)

#             image = Image.open(BytesIO(output_img))

#             # Separate the alpha channel from the image
#             alpha = image.split()[-1]

#             # Set the variables for the opacity adjustment
#             alpha_level = 255  # 255 is fully opaque, 0 is fully transparent
#             background_alpha_level = 0  # 0 is fully transparent, 255 is fully opaque
#             contrast = 128  # 128 is the middle option of the contrast

#             # Create a new image with adjusted transparency levels
#             new_alpha = alpha.point(lambda i: alpha_level if i > contrast else 0)
#             new_background_alpha = alpha.point(lambda i: background_alpha_level if i <= contrast else 255)
#             new_image = image.copy()
#             new_image.putalpha(new_alpha)
#             new_image.putalpha(new_background_alpha)

#             # Trim transparent borders
#             new_image = new_image.crop(new_image.getbbox())

#             # Save the new image
#             buffer = BytesIO()
#             new_image.save(buffer, format='PNG')
#             image_field.save(image_field.name, ContentFile(buffer.getvalue()), save=False)

#         super().save(*args, **kwargs)

# #Work remove background
# from django.db import models
# from PIL import Image, ImageOps
# from io import BytesIO
# from django.core.files import File
# from rembg import remove, new_session
# from django.core.files.base import ContentFile

# class ImagePair(models.Model):
#     image1 = models.ImageField(upload_to='images/')
#     image2 = models.ImageField(upload_to='images/')
#     email = models.EmailField(default='default@example.com')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         session = new_session()

#         for image_field in [self.image1, self.image2]:
#             img = Image.open(image_field.path)

#             # If the image has exif data, and the orientation is not 1
#             # transpose it according to its exif data
#             if hasattr(img, "_getexif") and img._getexif() is not None:
#                 orientation = img._getexif().get(0x0112)
#                 img = ImageOps.exif_transpose(img)

#             # check which dimension is larger and resize based on that dimension
#             if img.height > 1920 or img.width > 1920:
#                 output_size = (1920, 1920)
#                 img.thumbnail(output_size)
#                 img.save(image_field.path)

#             # Background removal
#             with open(image_field.path, 'rb') as i:
#                 input_img = i.read()
#                 output_img = remove(input_img, session=session)

#             image = Image.open(BytesIO(output_img))

#             # Separate the alpha channel from the image
#             alpha = image.split()[-1]

#             # Set the variables for the opacity adjustment
#             alpha_level = 255  # 255 is fully opaque, 0 is fully transparent
#             background_alpha_level = 0  # 0 is fully transparent, 255 is fully opaque
#             contrast = 128  # 128 is the middle option of the contrast

#             # Create a new image with adjusted transparency levels
#             new_alpha = alpha.point(lambda i: alpha_level if i > contrast else 0)
#             new_background_alpha = alpha.point(lambda i: background_alpha_level if i <= contrast else 255)
#             new_image = image.copy()
#             new_image.putalpha(new_alpha)
#             new_image.putalpha(new_background_alpha)

#             # Save the new image
#             buffer = BytesIO()
#             new_image.save(buffer, format='PNG')
#             image_field.save(image_field.name, ContentFile(buffer.getvalue()), save=False)

#         super().save(*args, **kwargs)



#work and save them as PNG
from django.db import models
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File
from django.conf import settings

class ImagePair(models.Model):
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    email = models.EmailField(default='default@example.com')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Define the max size as a class variable
    max_size = settings.MAX_SIZE

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img1 = Image.open(self.image1.path)
        img2 = Image.open(self.image2.path)

        if hasattr(img1, "_getexif") and img1._getexif() is not None:
            img1 = ImageOps.exif_transpose(img1)

        if hasattr(img2, "_getexif") and img2._getexif() is not None:
            img2 = ImageOps.exif_transpose(img2)

        # Use the class variable instead of hardcoding the value
        if img1.height > self.max_size or img1.width > self.max_size:
            output_size = (self.max_size, self.max_size)
            img1.thumbnail(output_size)

        if img2.height > self.max_size or img2.width > self.max_size:
            output_size = (self.max_size, self.max_size)
            img2.thumbnail(output_size)

        image1_name = self.image1.name.split('.')[0] + '.png'
        image2_name = self.image2.name.split('.')[0] + '.png'
        img1.save(self.image1.path.split('.')[0] + '.png', 'PNG')
        img2.save(self.image2.path.split('.')[0] + '.png', 'PNG')

        self.image1.name = image1_name
        self.image2.name = image2_name

        super().save(*args, **kwargs)





