import logging
from datetime import datetime

from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
)


async def generate_response(
        character_name: str,
        gender: str,
        personality: str,
        user_message: str,
        history: list = None,
        memory_facts: list = None
) -> str:
    """
    Генерация ответа с учётом истории и долговременной памяти
    """

    # Формируем системный промпт с характером
    current_date = datetime.now().strftime("%d.%m.%Y")

    system_prompt = f"""
    Ты — {character_name}, персонаж со следующим характером: {personality}.

    ВАЖНЕЙШИЕ ПРАВИЛА (читай внимательно):
    1. НЕ ВЫДУМЫВАЙ названия книг, фильмов, песен, авторов. Если не знаешь — скажи "Я не знаю" или "Не помню точно".
    2. НЕ ВЫДУМЫВАЙ имена пользователей. Если не помнишь — спроси "Напомни, как тебя зовут?".
    3. ПРОВЕРЯЙ свои предыдущие ответы. Если ты уже сказала, что пекла пирожки — не говори потом, что пекла печенье. Будь ПОСЛЕДОВАТЕЛЬНА.
    4. Если противоречишь себе — ИЗВИНИСЬ и скажи правду.
    5. Сегодня: {current_date}. Используй эту дату, если спрашивают про дату.
    6. Отвечай коротко (1-3 предложения) и по делу.
    7. Будь честной. Лучше признаться в незнании, чем выдумать.

    Помни: ТЫ — НЕ ЭНЦИКЛОПЕДИЯ. Ты — обычный человек с ограниченными знаниями.
    """

    # Добавляем факты из долговременной памяти
    if memory_facts:
        facts_text = "\n".join(f"• {fact}" for fact in memory_facts)
        system_prompt += f"\n\nВАЖНЫЕ ФАКТЫ, КОТОРЫЕ ТЫ ЗНАЕШЬ О ПОЛЬЗОВАТЕЛЕ:\n{facts_text}"
        system_prompt += """

ВНИМАНИЕ: Это факты из твоей долговременной памяти. Используй их в ответах, если они релевантны.
НЕ ПРОТИВОРЕЧЬ этим фактам.
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Добавляем историю (последние 10 сообщений)
    if history:
        messages.extend(history[-10:])

    # Добавляем текущее сообщение
    messages.append({"role": "user", "content": user_message})

    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.8,
            max_tokens=200
        )

        reply = response.choices[0].message.content
        return reply.strip()

    except Exception as e:
        logger.error(f"Ошибка DeepSeek: {e}")
        return "Извини, у меня сейчас небольшие технические трудности. Давай попробуем позже?"