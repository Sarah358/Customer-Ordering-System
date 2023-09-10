from __future__ import absolute_import

import os

from celery import Celery

from ecommerce.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings.development")

app = Celery("ecommerce")

app.config_from_object("ecommerce.settings.development", namespace="CELERY"),

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
