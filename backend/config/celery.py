from __future__ import absolute_import
import os
from celery import Celery

# Django의 settings 모듈을 Celery가 인식할 수 있도록 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("backend")

# settings.py에서 celery관련 설정 불러옴
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
