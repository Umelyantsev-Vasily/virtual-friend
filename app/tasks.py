import logging
from celery import shared_task
from app.services.character_service import CharacterService
from app.services.message_service import MessageService
from app.core.database import AsyncSessionLocal
from app.config import settings
from telegram import Bot
import asyncio

logger = logging.getLogger(__name__)


@shared_task
def send_proactive_message(text: str):
    """Отправляет активное сообщение всем пользователям с персонажами"""
    try:
        # Создаём бота
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        # Получаем всех пользователей с персонажами
        async def send_messages():
            async with AsyncSessionLocal() as db:
                char_service = CharacterService(db)
                # Получаем всех пользователей
                characters = await char_service.get_all_characters()

                for character in characters:
                    try:
                        user_id = int(character.user_telegram_id)
                        await bot.send_message(
                            chat_id=user_id,
                            text=text,
                            parse_mode='Markdown'
                        )
                        logger.info(f"✅ Сообщение отправлено пользователю {user_id}")

                        # Сохраняем сообщение в историю
                        msg_service = MessageService(db)
                        await msg_service.save_assistant_message(
                            character_id=character.id,
                            content=text
                        )

                    except Exception as e:
                        logger.error(f"❌ Ошибка отправки пользователю {user_id}: {e}")

        # Запускаем асинхронную функцию
        asyncio.run(send_messages())

    except Exception as e:
        logger.error(f"❌ Ошибка в send_proactive_message: {e}")


@shared_task
def send_birthday_message():
    """Отправляет поздравления с днём рождения"""
    # TODO: реализовать проверку дней рождения из фактов
    pass


@shared_task
def send_motivation_message():
    """Отправляет мотивационное сообщение"""
    texts = [
        "🌟 Ты способен на большее, чем думаешь! Верь в себя! 💪",
        "🚀 Каждый день — это новая возможность стать лучше!",
        "🌈 Не бойся ошибок — они делают тебя сильнее!",
        "✨ Ты уникален и неповторим! Помни об этом! 💫",
        "🎯 Маленькие шаги каждый день приводят к большим победам!",
    ]
    import random
    text = random.choice(texts)
    send_proactive_message.delay(text)