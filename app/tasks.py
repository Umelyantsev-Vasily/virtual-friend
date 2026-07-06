import asyncio
from celery import shared_task
from telegram import Bot
from app.config import settings
from app.core.database import AsyncSessionLocal
from app.models.character import Character


@shared_task
def send_proactive_message(message: str):
    """Отправляет сообщение всем пользователям"""

    async def _send():
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            result = await db.execute(select(Character))
            characters = result.scalars().all()

            if not characters:
                print("⚠️ Нет пользователей для отправки")
                return

            for character in characters:
                try:
                    await bot.send_message(
                        chat_id=character.user_telegram_id,
                        text=f"🤗 {message}"
                    )
                    print(f"✅ Сообщение отправлено {character.user_telegram_id}")
                except Exception as e:
                    print(f"❌ Ошибка отправки {character.user_telegram_id}: {e}")

    asyncio.run(_send())