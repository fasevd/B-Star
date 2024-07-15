
# B-Star
The B-Star app is built on a Django server and provides a seamless experience for rendering images and creating realistic 3D parallax effects. It automatically installs the required conda environment within the project folder and sets the environment variables for ffmpeg, a video encoder.


# B-Star App

## Overview

The B-Star app is built on a Django server and provides a seamless experience for rendering images and creating realistic 3D parallax effects. It automatically installs the required conda environment within the project folder and sets the environment variables for ffmpeg, a video encoder.

## Folder Structure

- **Main Folder:** `C:\B-Star`
- **Temporary Blender's Cache Folder:** `C:\tmp`
- **Media Folder:** `C:\B-Star\billboardstar_2\app\media`
- **Ready Videos Storage:** `C:\B-Star\billboardstar_2\app\media\ready`

## Features

- **Automated Environment Setup:** The app automatically installs the conda environment and sets necessary environment variables.
- **Celery and Redis Integration:** Supports task queuing, allowing multiple photo uploads from different users simultaneously. Celery manages tasks one after another efficiently.
- **AI Background Removal and 3D Rendering:** Uploaded photos are processed to remove backgrounds with rembg, rendered in a 3D environment, and the final result is a realistic and perspective-accurate parallax effect.

## System Requirements

- **Operating System:** Windows
- **GPU:** NVidia GPU (required for AI rembg model)

## Usage Instructions

1. **Email Verification:**
   - Add your email to receive a verification code.
   - Enter the received code to verify your email.

2. **Photo Upload:**
   - Upload two photos. The photos can be in any orientation (portrait or landscape), but the subject of the photo should be clearly expressed.
   - Choose the "Debug" template from the dropdown menu. Note that the "TimesSquare_Drone" and "Times Square Casual" templates are not uploaded.
   - The app will process these photos by removing the background and rendering them in a 3D environment.

3. **Output:**
   - The final movie with a realistic parallax effect will be sent to your email.

## Configuration

Add the following values to your `settings.py` file located at `C:\B-Star\billboardstar_2\app\app\settings.py`:

```python
EMAIL_HOST_USER = 'sender@gmail.com'
EMAIL_HOST_PASSWORD = 'Ask_google_email_settings_automatic_app_authorization'
```

## Installation Instructions

1. Clone the repository to your C drive:
   ```sh
   git clone <repository_url> C:\B-Star
   ```

2. Navigate to the main folder:
   ```sh
   cd C:\B-Star
   ```

3. Run the initialization script:
   ```sh
   Initiate_The_App_111111111.bat
   ```

## Testing

After running the app, you can test it by opening the following link in your browser: [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

## Additional Information

- **Rendered Image Cache:** Rendered images from Blender are cached in the `C:\tmp` folder.
- **Temporary Storage:** Uploaded photos appear in `C:\B-Star\billboardstar_2\app\media\image_in_use` temporarily during processing.

- **YouTube:** https://youtu.be/J1lA7NLmSWA

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---
