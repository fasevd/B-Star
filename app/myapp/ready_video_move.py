import os
import re
import shutil
from django.contrib.auth.models import User
from django.contrib import messages

def move_video(input_folder, output_folder, email):
    # Get a list of files in the input folder
    files = os.listdir(input_folder)

    # Find the video file using regex
    video_pattern = r'\.mp4$'
    video_files = [file for file in files if re.search(video_pattern, file)]

    if len(video_files) == 0:
        print("No video file found in the input folder.")
        return

    # Get the first video file found
    video_file = video_files[0]

    # Construct the new filename based on the email
    new_filename = f"{email}.mp4"

    # Check if the file already exists in the output folder
    if os.path.exists(os.path.join(output_folder, new_filename)):
        # Add an index to the filename to avoid overwriting existing files
        index = 1
        while os.path.exists(os.path.join(output_folder, f"{email}_{index}.mp4")):
            index += 1
        new_filename = f"{email}_{index}.mp4"

    # Move the video file to the output folder and rename it
    video_file_path = os.path.join(input_folder, video_file)
    shutil.move(video_file_path, os.path.join(output_folder, new_filename))

    # Now delete all remaining files in the input_folder
    remaining_files = os.listdir(input_folder)
    for file in remaining_files:
        file_path = os.path.join(input_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)  # remove the file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # remove dir and all contains

    print(f"The video file has been moved to {os.path.join(output_folder, new_filename)}")
    return new_filename


























# def move_video(input_folder, output_folder, email):
#     # Get a list of files in the input folder
#     files = os.listdir(input_folder)

#     # Find the video file using regex
#     video_pattern = r'\.mp4$'
#     video_files = [file for file in files if re.search(video_pattern, file)]

#     if len(video_files) == 0:
#         print("No video file found in the input folder.")
#         return

#     # Get the first video file found
#     video_file = video_files[0]

#     # Construct the new filename based on the email
#     new_filename = f"{email}.mp4"

#     # Check if the file already exists in the output folder
#     if os.path.exists(os.path.join(output_folder, new_filename)):
#         # Add an index to the filename to avoid overwriting existing files
#         index = 1
#         while os.path.exists(os.path.join(output_folder, f"{email}_{index}.mp4")):
#             index += 1
#         new_filename = f"{email}_{index}.mp4"

#     # Move the video file to the output folder and rename it
#     video_file_path = os.path.join(input_folder, video_file)
#     shutil.move(video_file_path, os.path.join(output_folder, new_filename))

#     print(f"The video file has been moved to {os.path.join(output_folder, new_filename)}")
#     return new_filename


