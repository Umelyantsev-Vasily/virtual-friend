import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


class MenuHandlers:
    """Обработчики меню"""

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user = update.effective_user

        # Проверяем есть ли персонаж (подставьте свою логику)
        has_character = False  # Замените на проверку из вашей БД

        welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в Frends - твоего виртуального друга.

📝 Создай своего персонажа и начни общение!
        """

        await update.message.reply_text(
            welcome_text,
            reply_markup=MenuKeyboard.main_menu(has_character)
        )

    @staticmethod
    async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Информация о боте"""
        text = """
🤖 **О боте Frends**

Это твой виртуальный друг на основе ИИ.

**Возможности:**
• 💬 Общение в любое время
• 🧠 Запоминание важных фактов
• 🎭 Уникальный характер персонажа
• ❤️ Эмоциональная поддержка

**Технологии:** DeepSeek AI, PostgreSQL, ChromaDB
        """
        await update.message.reply_text(text, parse_mode='Markdown')

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Помощь"""
        text = """
❓ **Помощь**

**Команды:**
/start - Главное меню
/cancel - Отменить действие

**Как создать персонажа:**
1. Нажми "📝 Создать персонажа"
2. Введи имя
3. Выбери пол и возраст
4. Опиши характер

**Советы:**
• Общайся чаще - я запоминаю факты о тебе
• Рассказывай о своих интересах
• Меняй персонажа когда хочешь

По всем вопросам: @support_bot
        """
        await update.message.reply_text(text, parse_mode='Markdown')