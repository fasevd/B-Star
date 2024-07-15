import os
from pathlib import Path
from bpy import context, ops, data, types
from django.conf import settings

def process_images(image_pair):
    # Load images and create the video using Blender
    # Save the video file in the media folder and return its URL
    pass  # Replace this line with your implementation

def get_media_path(file_name):
    return os.path.join(settings.MEDIA_ROOT, file_name)