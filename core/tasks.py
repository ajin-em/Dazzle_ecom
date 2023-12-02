# from celery import shared_task
# from django.core.mail import send_mail
# import random
# from django.conf import settings
# from .views import *

# @shared_task
# def send_otp_email(email):
#     # Generate OTP
#     otp = generated_otp

#     # Send OTP to email
#     send_mail(
#         'Your OTP for Registration',
#         f'Your OTP is: {generated_otp}',
#         settings.EMAIL_HOST_USER,
#         [email],
#         fail_silently=False,
#     )