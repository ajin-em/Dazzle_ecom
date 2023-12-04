from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dazzleumbrella.settings")
# app = Celery("dazzleumbrella")

# #we are using asia/kolkata time so we are making it False
# app.conf.enable_utc=False
# app.conf.update(timezone='Asia/Kolkata')

# app.config_from_object("django.conf:settings", namespace="CELERY")

# # app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# # @app.task(bind=True)
# # def debug_task(self):
# #     print(f"Request: {self.request!r}")
# if __name__ == "__main__":
#     app.start()


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dazzleumbrella.settings')

app = Celery('dazzleumbrella')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


