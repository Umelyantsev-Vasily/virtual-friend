import aiohttp
from app.config import settings


async def generate_response(character_name: str, personality: str, user_message: str) -> str:
    """
    Генерация ответа от лица персонажа через YandexGPT.
    """
    system_prompt = f"""
    Ты - {character_name}.
    Твой характер: {personality}.

    Правила:
    1. Отвечай как живой человек, коротко (1-3 предложения)
    2. Будь добрым и поддерживающим
    3. Не говори "я бот" или "я ИИ"
    4. Отвечай на русском языке
    """

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }

    model_uri = f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite"

    payload = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.8,
            "maxTokens": 200
        },
        "messages": [
            {"role": "system", "text": system_prompt},
            {"role": "user", "text": user_message}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"YandexGPT API error {response.status}: {error_text}")

            result = await response.json()
            reply = result["result"]["alternatives"][0]["message"]["text"]
            return reply.strip()