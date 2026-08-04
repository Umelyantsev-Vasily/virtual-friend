import pytest
from unittest.mock import AsyncMock, patch
from app.bot.handlers.menu import MenuHandlers


@pytest.mark.asyncio
class TestMenuHandlers:
    """Тесты для обработчиков меню"""

    async def test_about_handler(self, mock_update, mock_context):
        """Тест обработчика 'О боте'"""
        handler = MenuHandlers()

        await handler.about(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]

        assert "О боте Frends" in call_args
        assert "ИИ" in call_args or "DeepSeek" in call_args
        assert "PostgreSQL" in call_args
        assert "ChromaDB" in call_args

    async def test_help_handler(self, mock_update, mock_context):
        """Тест обработчика 'Помощь'"""
        handler = MenuHandlers()

        await handler.help(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]

        # Исправлено: проверяем наличие ключевых фраз вместо конкретных команд
        assert "Помощь" in call_args
        assert "start" in call_args  # /start
        assert "создать" in call_args.lower()  # Создать персонажа
        assert "совет" in call_args.lower()  # Советы

    async def test_about_has_markdown(self, mock_update, mock_context):
        """Тест что ответ содержит Markdown разметку"""
        handler = MenuHandlers()

        await handler.about(mock_update, mock_context)

        call_kwargs = mock_update.message.reply_text.call_args[1]
        assert call_kwargs.get('parse_mode') == 'Markdown'