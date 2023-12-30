from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from dazzleumbrella.celery import app

@shared_task
def account_verification_email(email, otp):
  subject = 'Account verification OTP'
  message = ''
  from_email = settings.EMAIL_HOST_USER
  recipient_list = [email]
  print(recipient_list)
  print(otp,'jhfdsdf')
  html_content = render_to_string('sendmail.html',{'otp':otp})
  send_mail(subject,message,from_email,recipient_list,html_message=html_content)

