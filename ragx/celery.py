import os

from celery import Celery
from django.conf import settings

from main.utils.log import get_logger

# Set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ragx.settings")
logger = get_logger("ragx.celery")

app = Celery("ragx")

app.conf.update(
    broker_url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    result_backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=False,
    # task_routes={
    #     "ragx.tasks.add": {
    #         "queue": "hipri"
    #     },
    # },
    # task_annotations={"tasks.add": {
    #     "rate_limit": "10/m"
    # }},
)

# Using a string here means the worker doesn"t have to serialize
# the configuration object to child processes.
# - namespace="CELERY" means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# app.config_from_object(f"django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
