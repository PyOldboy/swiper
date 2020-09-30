import os

from celery import Celery, platforms

from tasks import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantan.settings')

celery_app = Celery('tasks')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True