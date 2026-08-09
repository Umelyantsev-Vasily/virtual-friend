from telegram import Update
from telegram.ext import ContextTypes
from app.bot.keyboards.menu import MenuKeyboard

async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать настройки"""
    settings_text = """
⚙️ **Настройки**

Доступные опции:
• 🔄 Сменить персонажа — /reset
• 🗑 Удалить все данные — /reset
• 📝 Создать нового персонажа — /new

**Совет:** 
Чем больше ты общаешься, тем лучше я тебя понимаю!
"""

    await update.message.reply_text(
        settings_text,
        parse_mode='Markdown',
        reply_markup=MenuKeyboard.main_menu(True)
    )