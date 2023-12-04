# from __future__ import absolute_import  
# import smtplib
# from conf.celery import app
# from django.core import mail
# from django.template.loader import render_to_string  
# from django.conf import settings

# @app.task
# def send_email(to_email, subject, message):  
#     from_email = 'settings.EMAIL_HOST_USER'  
#     recipient_list = [to_email]  
#     html_message = render_to_string('email_template.html', {'message': message})  
#     try:  
#         mail.send_mail(subject, message, from_email, recipient_list, html_message=html_message)  
#     except smtplib.SMTPException as e:  
#         return 0  
#     return mail