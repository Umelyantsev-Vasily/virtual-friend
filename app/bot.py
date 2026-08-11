import sys
import os
from app.utils.message_utils import send_message_live
from app.bot.keyboards.menu import MenuKeyboard
from app.bot.handlers.menu import MenuHandlers

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
import asyncio
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.config import settings
from app.services.ai_service import generate_response
from app.services.character_service import CharacterService
from app.services.message_service import MessageService
from app.services.memory_service import MemoryService
from app.core.database import AsyncSessionLocal

# Импорты из handlers
from app.bot.handlers.profile import show_profile
from app.bot.handlers.dialog import show_dialog
from app.bot.handlers.settings import show_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Список случайных фактов для приветствия
WELCOME_FACTS = [
    "🐱 У тебя появился новый друг!",
    "🌍 Ты теперь не один — у тебя есть виртуальный собеседник!",
    "🚀 Начинаем путешествие в мир общения!",
    "💡 Знаешь, лучшие разговоры начинаются с простого 'Привет'!",
    "🌟 Твой новый друг уже ждёт твоего сообщения!",
    "🎉 Поздравляю! Ты только что приобрёл нового цифрового друга!",
    "🧠 Готов к интересным разговорам и неожиданным вопросам?",
    "🌻 Иногда лучший друг — тот, кто всегда готов выслушать.",
    "☕️ Представь, что вы сидите в уютном кафе и разговариваете...",
    "📚 Каждый диалог — это новая история. Начни свою!",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие с меню"""
    user = update.effective_user
    user_id = str(user.id)

    async with AsyncSessionLocal() as db:
        service = CharacterService(db)
        character = await service.get_by_user_id(user_id)
        has_character = character is not None

    welcome_text = f"""
👋 **Привет, {user.first_name}!**

Добро пожаловать в Frends — твоего виртуального друга.

"""
    if has_character:
        welcome_text += f"""
🌟 Твой друг **{character.name}** уже ждёт тебя!
Просто напиши что-нибудь, чтобы начать диалог 💬
        """
    else:
        welcome_text += """
📝 Создай своего персонажа и начни общение!

Нажми кнопку "Создать персонажа" ниже.
        """

    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=MenuKeyboard.main_menu(has_character)
    )


async def create_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание персонажа с элементами магии и случайности"""
    user_id = str(update.effective_user.id)

    async with AsyncSessionLocal() as db:
        service = CharacterService(db)
        existing = await service.get_by_user_id(user_id)
        if existing:
            await update.message.reply_text(
                f"🔮 Ты уже связан с **{existing.name}**.\n"
                f"Судьба не любит перемен — останься верным другу! 💫"
            )
            return

        await update.message.reply_text("🔮 **Открываю портал в мир дружбы...**", parse_mode="Markdown")
        await asyncio.sleep(0.8)

        await update.message.reply_text("⚡️ **Вызываю твоего идеального собеседника...**", parse_mode="Markdown")
        await asyncio.sleep(0.6)

        await update.message.reply_text("🌟 **Персонаж готов!**", parse_mode="Markdown")
        await asyncio.sleep(0.3)

        character = await service.create_default_character(user_id)

        welcome_message = (
            f"🌌 **Из бездны данных родился твой друг!**\n\n"
            f"🔄 **Синхронизация завершена**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📡 **Имя:** `{character.name}`\n"
            f"⏳ **Возраст:** `{character.age}`\n"
            f"⚧️ **Пол:** `{character.gender}`\n"
            f"🧬 **Характер:** `{character.personality}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔮 **Его миссия:**\n"
            f"• Быть рядом в любой момент\n"
            f"• Слушать без осуждения\n"
            f"• Поддерживать, даже когда трудно\n\n"
            f"✨ **Первый шаг:**\n"
            f"Просто скажи **«Привет»**, и начнётся магия 💫"
        )

        await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def new_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создание нового персонажа через диалог"""
    user_id = str(update.effective_user.id)

    async with AsyncSessionLocal() as db:
        service = CharacterService(db)
        character = await service.get_by_user_id(user_id)

        if character:
            await update.message.reply_text(
                f"⚠️ У тебя уже есть персонаж {character.name}.\n"
                f"Сначала удали его командой /reset"
            )
            return

    await update.message.reply_text(
        "🎭 Давай создадим нового персонажа!\n\n"
        "1️⃣ Отправь имя персонажа (например: Анна):",
        reply_markup=MenuKeyboard.cancel()
    )
    context.user_data['creating_character'] = True


async def handle_character_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка диалога создания персонажа (с очисткой памяти)"""
    user_id = str(update.effective_user.id)
    text = update.message.text

    if not context.user_data.get('creating_character'):
        return

    if 'character_name' not in context.user_data:
        context.user_data['character_name'] = text
        await update.message.reply_text(
            f"✅ Имя: {text}\n\n"
            f"2️⃣ Укажи возраст (только число, например: 25):"
        )
        return

    if 'character_age' not in context.user_data:
        try:
            age = int(text)
            if age < 1 or age > 120:
                await update.message.reply_text("❌ Возраст должен быть от 1 до 120. Попробуй ещё раз:")
                return
            context.user_data['character_age'] = age
            await update.message.reply_text(
                f"✅ Возраст: {age}\n\n"
                f"3️⃣ Выбери пол персонажа:\n"
                f"   Отправь: Мужской, Женский или Другой"
            )
        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, введи число. Например: 25")
        return

    if 'character_gender' not in context.user_data:
        gender = text.lower()
        if gender in ['мужской', 'женский', 'другой', 'муж', 'жен', 'м', 'ж', 'д']:
            gender_map = {
                'муж': 'Мужской', 'жен': 'Женский',
                'м': 'Мужской', 'ж': 'Женский',
                'д': 'Другой', 'другой': 'Другой'
            }
            context.user_data['character_gender'] = gender_map.get(gender, gender.capitalize())
            await update.message.reply_text(
                f"✅ Пол: {context.user_data['character_gender']}\n\n"
                f"4️⃣ Опиши характер персонажа (например: весёлая, заботливая и дружелюбная):"
            )
        else:
            await update.message.reply_text(
                "❌ Пожалуйста, выбери: Мужской, Женский или Другой"
            )
        return

    if 'character_personality' not in context.user_data:
        context.user_data['character_personality'] = text
        await update.message.reply_text(
            f"✅ Характер: {text}\n\n"
            f"🎉 Отлично! Создаю персонажа..."
        )

        async with AsyncSessionLocal() as db:
            service = CharacterService(db)

            existing = await service.get_by_user_id(user_id)
            if existing:
                memory_service = MemoryService(db, existing.id)
                await memory_service.clear_all()
                await service.delete_character(existing.id)

            new_character = await service.create_custom_character(
                user_telegram_id=user_id,
                name=context.user_data['character_name'],
                age=context.user_data['character_age'],
                gender=context.user_data['character_gender'],
                personality=context.user_data['character_personality']
            )

            context.user_data.pop('creating_character', None)
            context.user_data.pop('character_name', None)
            context.user_data.pop('character_age', None)
            context.user_data.pop('character_gender', None)
            context.user_data.pop('character_personality', None)

            await update.message.reply_text(
                f"✅ Создан новый персонаж: {new_character.name}!\n"
                f"Возраст: {new_character.age}\n"
                f"Пол: {new_character.gender}\n"
                f"Характер: {new_character.personality}\n\n"
                f"Теперь можешь общаться со мной! Просто напиши что-нибудь 💬"
            )


async def reset_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сброс персонажа с подтверждением"""
    user_id = str(update.effective_user.id)

    async with AsyncSessionLocal() as db:
        service = CharacterService(db)
        character = await service.get_by_user_id(user_id)

        if not character:
            await update.message.reply_text("У тебя еще нет персонажа! Создай его командой /create")
            return

        context.user_data['reset_character_id'] = character.id

        await update.message.reply_text(
            f"⚠️ Ты действительно хочешь удалить персонажа {character.name}?\n"
            f"Это действие НЕЛЬЗЯ будет отменить!\n\n"
            f"📌 Если уверен — отправь: /confirm_reset\n"
            f"📌 Если передумал — просто продолжай общаться"
        )


async def confirm_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение сброса персонажа с очисткой памяти"""
    user_id = str(update.effective_user.id)

    reset_id = context.user_data.get('reset_character_id')
    if not reset_id:
        await update.message.reply_text("⚠️ Ты не начинал сброс персонажа. Отправь /reset")
        return

    async with AsyncSessionLocal() as db:
        service = CharacterService(db)
        character = await service.get_by_user_id(user_id)

        if not character or character.id != reset_id:
            await update.message.reply_text("❌ Ошибка: персонаж не найден")
            return

        memory_service = MemoryService(db, character.id)
        await memory_service.clear_all()

        await service.delete_character(character.id)

        context.user_data.pop('reset_character_id', None)

        await update.message.reply_text(
            f"✅ Персонаж {character.name} удалён.\n"
            f"Ты можешь создать нового командой /create или /new"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка всех сообщений"""
    user_id = str(update.effective_user.id)
    user_message = update.message.text

    # === ОБРАБОТКА КНОПОК МЕНЮ ===

    if user_message == "❌ Отмена":
        context.user_data.pop('creating_character', None)
        context.user_data.pop('character_name', None)
        context.user_data.pop('character_age', None)
        context.user_data.pop('character_gender', None)
        context.user_data.pop('character_personality', None)

        async with AsyncSessionLocal() as db:
            service = CharacterService(db)
            character = await service.get_by_user_id(user_id)
            has_character = character is not None

        await update.message.reply_text(
            "❌ Действие отменено",
            reply_markup=MenuKeyboard.main_menu(has_character)
        )
        return

    if user_message == "📝 Создать персонажа":
        await create_character(update, context)
        return

    if user_message == "💬 Диалог":
        await show_dialog(update, context)
        return

    if user_message in ["👤 Профиль", "👤 Мой профиль"]:
        await show_profile(update, context)
        return

    if user_message == "🔄 Сменить персонажа":
        await reset_character(update, context)
        return

    if user_message == "⚙️ Настройки":
        await show_settings(update, context)
        return

    # Обработка "Ещё!" для цитат (гибкая проверка)
    if "ещё" in user_message.lower() and context.user_data.get('quote_mode'):
        await show_dialog(update, context)
        return

    # === СОЗДАНИЕ ПЕРСОНАЖА ===
    if context.user_data.get('creating_character'):
        await handle_character_creation(update, context)
        return

    # === ОСНОВНОЙ ДИАЛОГ ===
    async with AsyncSessionLocal() as db:
        char_service = CharacterService(db)
        msg_service = MessageService(db)

        character = await char_service.get_by_user_id(user_id)
        if not character:
            await update.message.reply_text(
                "❌ У тебя еще нет персонажа!\nСоздай его через /create или нажми '📝 Создать персонажа'",
                reply_markup=MenuKeyboard.main_menu(False)
            )
            return

        await msg_service.save_user_message(character.id, user_message)
        history = await msg_service.get_history_for_ai(character.id, limit=20)

        memory_service = MemoryService(db, character.id)
        memory_facts = await memory_service.get_relevant_facts(user_message, limit=5)

        try:
            ai_reply = await generate_response(
                character_name=character.name,
                gender=character.gender,
                personality=character.personality,
                user_message=user_message,
                history=history,
                memory_facts=memory_facts
            )
        except Exception as e:
            logger.error(f"Ошибка AI: {e}")
            ai_reply = "Извини, у меня сейчас небольшие технические трудности. Давай попробуем позже?"

        await msg_service.save_assistant_message(character.id, ai_reply)

        try:
            memory_service = MemoryService(db, character.id)
            patterns = [
                (r'(?:меня зовут|я\s+)([А-Яа-яЁё\s]+?)(?:[,\.]|$)', "Имя пользователя: {}"),
                (r'(?:мне|мне\s+)?(\d{1,2})\s*(?:лет|года|год)', "Возраст пользователя: {}"),
                (r'день рождения\s+(\d{1,2}\s+[а-яА-ЯёЁ]+\s+\d{4})', "День рождения пользователя: {}"),
                (r'я (?:люблю|обожаю)\s+([а-яА-ЯёЁ\s,]+?)(?:[.,!?]|$)', "Пользователь любит: {}"),
                (r'(?:хобби|увлекаюсь|занимаюсь)\s+([а-яА-ЯёЁ\s,]+?)(?:[.,!?]|$)', "Увлечение пользователя: {}"),
                (r'(?:работаю|профессия)\s+([а-яА-ЯёЁ\s]+?)(?:[.,!?]|$)', "Профессия пользователя: {}"),
                (r'(?:живу|город)\s+([а-яА-ЯёЁ\s]+?)(?:[.,!?]|$)', "Город пользователя: {}"),
            ]
            for pattern, template in patterns:
                match = re.search(pattern, user_message, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if len(value) > 2:
                        await memory_service.add_fact(template.format(value))
                        logger.info(f"Сохранено: {template.format(value)}")
        except Exception as e:
            logger.error(f"Ошибка сохранения факта: {e}")

        # === ОТПРАВКА С ЭФФЕКТОМ ЖИВОГО ДИАЛОГА ===
        await send_message_live(
            update,
            ai_reply,
            delay=1.2,
            reply_markup=MenuKeyboard.main_menu(True)
        )


def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не найден в .env")
        return

    app = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .base_url("https://telegram-api-proxy.virtual-friend-telegram-proxy.workers.dev/bot")
        .connect_timeout(60.0)
        .read_timeout(60.0)
        .write_timeout(60.0)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create", create_character))
    app.add_handler(CommandHandler("new", new_character))
    app.add_handler(CommandHandler("reset", reset_character))
    app.add_handler(CommandHandler("confirm_reset", confirm_reset))

    menu = MenuHandlers()
    app.add_handler(MessageHandler(filters.Regex('^ℹ️ О боте$'), menu.about))
    app.add_handler(MessageHandler(filters.Regex('^❓ Помощь$'), menu.help))

    app.add_handler(MessageHandler(filters.Regex('^📝 Создать персонажа$'), create_character))
    app.add_handler(MessageHandler(filters.Regex('^👤 (Мой )?Профиль$'), show_profile))
    app.add_handler(MessageHandler(filters.Regex('^🔄 Сменить персонажа$'), reset_character))
    app.add_handler(MessageHandler(filters.Regex('^⚙️ Настройки$'), show_settings))
    app.add_handler(MessageHandler(filters.Regex('^💬 Диалог$'), show_dialog))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Telegram бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()