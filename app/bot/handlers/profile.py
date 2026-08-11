import logging
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.keyboards.menu import MenuKeyboard
from app.services.character_service import CharacterService
from app.services.message_service import MessageService
from app.services.memory_service import MemoryService
from app.core.database import AsyncSessionLocal
from app.utils.message_utils import send_message_live

logger = logging.getLogger(__name__)

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать профиль пользователя"""
    user_id = str(update.effective_user.id)

    async with AsyncSessionLocal() as db:
        char_service = CharacterService(db)
        msg_service = MessageService(db)

        character = await char_service.get_by_user_id(user_id)
        if not character:
            await update.message.reply_text(
                "❌ У тебя еще нет персонажа!",
                reply_markup=MenuKeyboard.main_menu(False)
            )
            return

        history = await msg_service.get_history(character.id, limit=100)
        total_messages = len(history)

        memory_service = MemoryService(db, character.id)
        facts = await memory_service.get_all_facts()

        profile_text = f"""
👤 **Твой профиль**

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 **Персонаж:** {character.name}
⏳ **Возраст:** {character.age}
⚧️ **Пол:** {character.gender}
🧬 **Характер:** {character.personality}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **Статистика:**
• 💬 Сообщений: {total_messages}
• 🧠 Фактов в памяти: {len(facts)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        if facts:
            profile_text += "\n🧩 **Что я знаю о тебе:**\n"
            for fact in facts[:5]:
                profile_text += f"• {fact}\n"
            if len(facts) > 5:
                profile_text += f"• ...и еще {len(facts) - 5} фактов\n"

        await send_message_live(
            update,
            profile_text,
            parse_mode='Markdown',
            reply_markup=MenuKeyboard.main_menu(True)
        )