from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery(
    "virtual_friend",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    beat_schedule={
        "morning_message": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=9, minute=0),
            "args": ("Доброе утро! Хорошего дня! ☀️",),
        },
        "evening_message": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=20, minute=0),
            "args": ("Как прошёл твой день? Расскажи! 🌙",),
        },
    },
)

celery_app.autodiscover_tasks(['app.tasks'])