from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def account_verification_email(email,otp):
  subject = 'Account verification OTP'
  message = ''
  from_email = settings.EMAIL_HOST_USER
  recipient_list = [email]
  html_content = render_to_string('sendmail.html',{'otp':otp})
  send_mail(subject,message,from_email,recipient_list,html_message=html_content)

