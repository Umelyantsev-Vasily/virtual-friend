import re
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def send_message_live(
        update: Update,
        text: str,
        delay: float = None,  # None = автоматический расчёт
        min_length: int = 80,
        parse_mode: str = None,
        reply_markup=None
):
    """
    Отправляет сообщение по частям с эффектом живого диалога.
    Скорость печатания зависит от длины сообщения.

    Args:
        update: Update объект
        text: Текст для отправки
        delay: Задержка между сообщениями (если None - рассчитывается автоматически)
        min_length: Минимальная длина для разбивки
        parse_mode: Режим парсинга (Markdown, HTML)
        reply_markup: Клавиатура
    """
    # Если текст короткий - отправляем сразу
    if len(text) < min_length:
        await update.message.reply_text(
            text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        return

    # Разбиваем на предложения
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Если одно предложение или меньше 3 - отправляем сразу
    if len(sentences) <= 1 or len(sentences) < 3:
        await update.message.reply_text(
            text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        return

    # Рассчитываем задержку в зависимости от длины
    if delay is None:
        total_chars = len(text)
        if total_chars < 150:
            delay = 0.8
        elif total_chars < 300:
            delay = 1.2
        elif total_chars < 500:
            delay = 1.8
        elif total_chars < 800:
            delay = 2.5
        else:
            delay = 3.0

    # Показываем "печатает..."
    await update.message.reply_chat_action(action="typing")
    await asyncio.sleep(0.5)

    # Отправляем первое предложение
    first_msg = sentences[0]
    await update.message.reply_text(
        first_msg,
        parse_mode=parse_mode
    )

    # Остальные с задержкой
    for i, sentence in enumerate(sentences[1:], 1):
        await asyncio.sleep(delay)
        await update.message.reply_chat_action(action="typing")
        await asyncio.sleep(0.3)

        # Если последнее сообщение и есть клавиатура - добавляем её
        if i == len(sentences) - 1 and reply_markup:
            await update.message.reply_text(
                sentence,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                sentence,
                parse_mode=parse_mode
            )