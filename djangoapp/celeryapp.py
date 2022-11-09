from __future__ import absolute_import
import os

from celery import Celery

from djangoapp.settings import env, ENVIRONMENT


"""
Celery app configuration
celery -A djangoapp.celeryapp worker -Q email,sms -E --loglevel=INFO
"""

celery_backend = env('CELERY_BACKEND', default='redis://localhost:6379/0')
celery_broker = env('CELERY_BROKER', default='amqp://guest:guest@localhost:5672//')

# To register task into worker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapp.settings')

app = Celery('djangoapp.celeryapp', backend=celery_backend, broker=celery_broker)

