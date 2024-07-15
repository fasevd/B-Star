# views.py
from time import time, sleep
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
# from django.utils.crypto import get_random_string
from django.conf import settings
import logging

from .forms import ImagePairForm
from .models import ImagePair
from .tasks import process_images_and_render_video

# Get an instance of a logger
logger = logging.getLogger(__name__)

def enter_email(request):
    if request.method == 'POST':
        request.session.update({
            'email': request.POST.get('email'),  # Store email in session
            'code': get_random_string(length=2, allowed_chars='0123456789')
            # 'code': get_random_string(length=4)  # Store code in session
        })
        request.session.modified = True  # Mark session as modified to ensure changes are saved
        send_mail('Your confirmation code',
                  f"Here is your confirmation code: {request.session['code']}",
                  settings.EMAIL_HOST_USER,
                  [request.session['email']],
                  fail_silently=False)
        return redirect('enter_code')
    return render(request, 'enter_email.html')

def enter_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        # check if the entered_code matches the code in your session for the user or if it is "6666"
        if entered_code in (request.session.get('code'), "6666"):
            return redirect('home')
        else:
            email = request.session.get('email')
            attempts = cache.get(email, 0)
            last_try_time = cache.get(f'{email}_time', time())
            
            if attempts >= 3 and time() - last_try_time < 60:
                wait_time = 60 - int(time() - last_try_time)
                messages.error(request, f'You have made too many attempts. Please try again after {wait_time} seconds.')
            else:
                cache.set(email, attempts + 1, 60)
                cache.set(f'{email}_time', time(), 60)
                messages.error(request, 'Invalid code.')
    return render(request, 'enter_code.html')

def logout(request):
    for key in ['email', 'code']:
        request.session.pop(key, None)  # Remove email and code from session
    request.session.modified = True  # Mark session as modified to ensure changes are saved
    return redirect('enter_email')

def home(request):
    email = request.session.get('email')  # Retrieve email from session
    if not email:
        return redirect('enter_email')  # Redirect to get email if not available in session
    form = ImagePairForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        image_pair = form.save()
        template_key = form.cleaned_data['template']
        template_path = settings.TEMPLATE_PATHS.get(template_key)
        process_images_and_render_video.delay(image_pair.image1.name, image_pair.image2.name, email, template_path)  # pass the email to the task
        messages.info(request, 'Your request is being processed. You will be notified by email within 3-5 minutes when the video is ready.')
        return redirect('home')  # redirect back to the same page to show the message
    if form.errors:
        logger.info('Form errors: %s', form.errors)
    return render(request, 'home.html', {'form': form, 'email': email})









# from django.shortcuts import render
# from .forms import ImagePairForm
# from .models import ImagePair
# from .tasks import process_images_and_render_video
# from django.contrib import messages
# from django.shortcuts import render, redirect
# import logging
# from django.core.mail import send_mail
# from django.contrib import messages
# from django.utils.crypto import get_random_string
# from django.conf import settings
# # Get an instance of a logger
# logger = logging.getLogger(__name__)


# def enter_email(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         request.session['email'] = email  # Store email in session
#         code = get_random_string(length=6)
#         request.session['code'] = code  # Store code in session
#         request.session.modified = True  # Mark session as modified to ensure changes are saved

#         # save the code in your database associated with the user
#         # send the code via email
#         send_mail(
#             'Your confirmation code',
#             f'Here is your confirmation code: {code}',
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )
#         return redirect('enter_code')
#     return render(request, 'enter_email.html')

# def enter_code(request):
#     if request.method == 'POST':
#         entered_code = request.POST.get('code')

#         # check if the entered_code matches the code in your session for the user or if it is "666666"
#         if 'code' in request.session and (entered_code == request.session['code'] or entered_code == "666666"):
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid code.')
#     return render(request, 'enter_code.html')


# def logout(request):
#     request.session.pop('email', None)  # Remove email from session
#     request.session.modified = True  # Mark session as modified to ensure changes are saved
#     return redirect('enter_email')  # or wherever you want to redirect after logout

# def home(request):
#     email = request.session.get('email')  # Retrieve email from session
#     if not email:
#         return redirect('enter_email')  # Redirect to get email if not available in session

#     if request.method == 'POST':
#         form = ImagePairForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_pair = form.save()
#             image1_name = image_pair.image1.name
#             image2_name = image_pair.image2.name
#             process_images_and_render_video.delay(image1_name, image2_name, email)  # pass the email to the task

#             messages.info(request, 'Your request is being processed. You will be notified when the video is ready.')
#             return redirect('home')  # redirect back to the same page to show the message
#         else:
#             logger.info('Form errors: %s', form.errors)

#     form = ImagePairForm()
#     return render(request, 'myapp/home.html', {'form': form, 'email': email})





























# def enter_email(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         request.session['email'] = email  # Store email in session
#         request.session.modified = True  # Mark session as modified to ensure changes are saved
#         code = get_random_string(length=6)
#         # save the code in your database associated with the user
#         # send the code via email
#         send_mail(
#             'Your confirmation code',
#             f'Here is your confirmation code: {code}',
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )
#         return redirect('enter_code')
#     return render(request, 'enter_email.html')

# def enter_code(request):
#     if request.method == 'POST':
#         entered_code = request.POST.get('code')
#         # check if the entered_code matches the code in your database for the user
#         # if yes:
#         return redirect('home')
#         # else:
#         messages.error(request, 'Invalid code.')
#     return render(request, 'enter_code.html')


# def home(request):
#     email = request.session.get('email')  # Retrieve email from session
#     if not email:
#         return redirect('enter_email')  # Redirect to get email if not available in session
    
#     if request.method == 'POST':
#         form = ImagePairForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_pair = form.save()

#             # Get the filenames of the images and the email
#             image1_name = image_pair.image1.name
#             image2_name = image_pair.image2.name
#             # email = image_pair.email  # assuming your model has an 'email' field

#             # Trigger the Celery task
#             process_images_and_render_video.delay(image1_name, image2_name, email)  # pass the email to the task

#             # request.session.pop('email', None)  # Remove email from session
#             # request.session.modified = True  # Mark session as modified to ensure changes are saved

#             # Show a message to the user that their request is being processed
#             messages.info(request, 'Your request is being processed. You will be notified when the video is ready.')
#             return redirect('home')  # redirect back to the same page to show the message
        
#         else:
#             # Log form errors
#             logger.info('Form errors: %s', form.errors)

#     form = ImagePairForm()
#     return render(request, 'myapp/home.html', {'form': form})




















# def home(request):
#     if request.method == 'POST':
#         form = ImagePairForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_pair = form.save()

#             # Get the filenames of the images and the email
#             image1_name = image_pair.image1.name
#             image2_name = image_pair.image2.name
#             email = image_pair.email  # assuming your model has an 'email' field
#             #BLUE - 
#             # Trigger the Celery task
#             process_images_and_render_video.delay(image1_name, image2_name, email)  # pass the email to the task

#             # After the task is triggered, we might not have the video_url immediately
#             # You might want to show a message to the user that their request is being processed
#             # And then use another mechanism (like email or websockets) to notify them when the video is ready
#             return render(request, 'myapp/home.html', {'form': form, 'message': 'Your request is being processed. You will be notified when the video is ready.'})

#     form = ImagePairForm()
#     return render(request, 'myapp/home.html', {'form': form})






