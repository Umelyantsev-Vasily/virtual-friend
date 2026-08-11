import logging
import random
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.keyboards.menu import MenuKeyboard
from app.services.character_service import CharacterService
from app.services.message_service import MessageService
from app.services.memory_service import MemoryService
from app.services.ai_service import generate_response
from app.core.database import AsyncSessionLocal
from app.utils.message_utils import send_message_live

logger = logging.getLogger(__name__)

async def show_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация цитаты через AI на основе диалога"""
    user_id = str(update.effective_user.id)

    async with AsyncSessionLocal() as db:
        char_service = CharacterService(db)
        msg_service = MessageService(db)

        character = await char_service.get_by_user_id(user_id)
        if not character:
            await update.message.reply_text(
                "❌ У тебя еще нет персонажа!\nСоздай его через /create",
                reply_markup=MenuKeyboard.main_menu(False)
            )
            return

        history = await msg_service.get_history(character.id, limit=30)
        total_messages = len(history)

        memory_service = MemoryService(db, character.id)
        facts = await memory_service.get_all_facts()

        user_texts = [msg.content for msg in history if msg.role == "user"]
        last_messages = "\n".join(user_texts[-5:]) if user_texts else "пока нет сообщений"
        facts_text = "\n".join(f"• {fact}" for fact in facts[:5]) if facts else "пока нет фактов"

        prompt = f"""
Ты - {character.name}, персонаж со следующими чертами:
- Характер: {character.personality}
- Пол: {character.gender}
- Возраст: {character.age}

Пользователь написал тебе такие сообщения (последние 5):
{last_messages}

Факты, которые ты запомнил о пользователе:
{facts_text}

Всего сообщений: {total_messages}

Задание: Сгенерируй **уникальную цитату дня** для этого пользователя.
Цитата должна быть:
1. Вдохновляющей или смешной
2. Персонализированной
3. Короткой (1-2 предложения)
4. В стиле твоего персонажа ({character.name})

Также добавь 2-3 причины, почему эта цитата подходит именно этому пользователю.
Ответ должен быть в формате:
ЦИТАТА: [текст цитаты]
ПРИЧИНЫ: [причина 1] | [причина 2] | [причина 3]
"""

        try:
            response_text = await generate_response(
                character_name=character.name,
                gender=character.gender,
                personality=character.personality,
                user_message=prompt,
                history=[],
                memory_facts=facts
            )

            quote = ""
            reasons = []
            for line in response_text.split('\n'):
                if line.startswith("ЦИТАТА:"):
                    quote = line.replace("ЦИТАТА:", "").strip()
                elif line.startswith("ПРИЧИНЫ:"):
                    reasons = [r.strip() for r in line.replace("ПРИЧИНЫ:", "").split("|") if r.strip()]

            if not quote:
                quote = response_text if response_text else "Жизнь — как диалог: главное не молчать! 😄"
            if not reasons:
                reasons = [
                    "• Ты уникальный человек 🌟",
                    "• Я чувствую твою энергию ⚡",
                    "• У нас уже хороший диалог 💬"
                ]

        except Exception as e:
            logger.error(f"Ошибка генерации цитаты: {e}")
            fallback_quotes = [
                "Жизнь — как программирование: если не работает, перезагрузи! 💻",
                "Будь собой — остальные роли уже заняты. 😎",
                "Улыбайся, даже если грустно — это бесплатно! 😊",
                "Сделай сегодня то, что другие не хотят, и завтра ты будешь жить как они не могут. 💪"
            ]
            quote = random.choice(fallback_quotes)
            reasons = [
                "• Ты заслуживаешь лучшего! 🌟",
                "• Я верю в твой потенциал! 🚀",
                "• Ты делаешь этот мир лучше! 💫"
            ]

        dialog_text = f"""
💬 **Цитата дня от {character.name}** ✨

📜 *"{quote}"*

━━━━━━━━━━━━━━━━━━━━━━━━━━━
😄 **Эта цитата подходит тебе, потому что:**
{chr(10).join(reasons)}

💡 **Хочешь ещё цитату?** Напиши **"Ещё!"**
"""

        context.user_data['quote_mode'] = True

        await send_message_live(
            update,
            dialog_text,
            delay=1.0,
            parse_mode='Markdown',
            reply_markup=MenuKeyboard.main_menu(True)
        )