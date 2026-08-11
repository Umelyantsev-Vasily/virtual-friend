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
        # Утро (9:00-10:00)
        "morning_greeting": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=9, minute=0),
            "args": ("🌅 Доброе утро! Как спалось? Надеюсь, сегодня будет отличный день! ☀️",),
        },
        # День (13:00-14:00)
        "afternoon_check": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=13, minute=30),
            "args": ("🍽️ Привет! Как прошла первая половина дня? Уже пообедал? 😊",),
        },
        # Вечер (19:00-20:00)
        "evening_check": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=19, minute=0),
            "args": ("🌇 Привет! Чем занимался сегодня? Хочешь поделиться чем-то интересным? ✨",),
        },
        # Поздний вечер (22:00-23:00) - только по пятницам и субботам
        "late_evening": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=22, minute=30, day_of_week='5,6'),
            "args": ("🌙 Вечер пятницы! Есть планы на выходные? Или просто отдыхаешь? 🎉",),
        },
        # Дневное вдохновение (16:00-17:00)
        "afternoon_inspiration": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=16, minute=0),
            "args": ("💪 Привет! Не забывай делать перерывы. Ты молодец, продолжай в том же духе! 🌟",),
        },
        # Уютный вечер (21:00-22:00) - не по пятницам и субботам
        "cozy_evening": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=21, minute=0, day_of_week='0-4'),
            "args": ("📚 Привет! Как прошёл день? Может, хочешь что-то обсудить? Я всегда рядом. 💫",),
        },
        # Субботнее утро (10:00-11:00)
        "saturday_morning": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=10, minute=0, day_of_week='6'),
            "args": ("🌞 Доброе субботнее утро! Какие планы на выходные? Может, почитаешь или прогуляешься? 📖",),
        },
        # Воскресное настроение (11:00-12:00)
        "sunday_morning": {
            "task": "app.tasks.send_proactive_message",
            "schedule": crontab(hour=11, minute=0, day_of_week='0'),
            "args": ("☀️ С добрым утром! Не забывай отдыхать и набираться сил перед новой неделей. 💆‍♂️",),
        },
    },
)

celery_app.autodiscover_tasks(['app.tasks'])