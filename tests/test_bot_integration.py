import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update


@pytest.mark.asyncio
class TestBotIntegration:
    """Интеграционные тесты бота"""

    @patch('app.bot.CharacterService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_start_command_without_character(self, mock_session, mock_char_service, mock_update, mock_context):
        """Тест команды /start без персонажа"""
        from app.bot import start

        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=None)
        mock_char_service.return_value = mock_char_instance

        await start(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Привет" in call_args
        assert "Создай" in call_args

    @patch('app.bot.CharacterService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_start_command_with_character(self, mock_session, mock_char_service, mock_update, mock_context,
                                                mock_character):
        """Тест команды /start с персонажем"""
        from app.bot import start

        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=mock_character)
        mock_char_service.return_value = mock_char_instance

        await start(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "Привет" in call_args
        assert mock_character.name in call_args

    @patch('app.bot.CharacterService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_handle_message_without_character(self, mock_session, mock_char_service, mock_update, mock_context):
        """Тест обработки сообщения без персонажа"""
        from app.bot import handle_message

        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=None)
        mock_char_service.return_value = mock_char_instance

        mock_update.message.text = "Привет!"

        await handle_message(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "У тебя еще нет персонажа" in call_args

    @patch('app.bot.CharacterService')
    @patch('app.bot.MessageService')
    @patch('app.bot.MemoryService')
    @patch('app.bot.generate_response')
    @patch('app.bot.AsyncSessionLocal')
    async def test_handle_message_with_character(
            self, mock_session, mock_generate, mock_memory, mock_msg, mock_char,
            mock_update, mock_context, mock_character
    ):
        """Тест обработки сообщения с персонажем"""
        from app.bot import handle_message

        # Настройка моков
        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=mock_character)
        mock_char.return_value = mock_char_instance

        mock_msg_instance = AsyncMock()
        mock_msg_instance.save_user_message = AsyncMock()
        mock_msg_instance.save_assistant_message = AsyncMock()
        mock_msg_instance.get_history_for_ai = AsyncMock(return_value=[])
        mock_msg.return_value = mock_msg_instance

        mock_memory_instance = AsyncMock()
        mock_memory_instance.get_relevant_facts = AsyncMock(return_value=[])
        mock_memory_instance.add_fact = AsyncMock()
        mock_memory_instance.get_all_facts = AsyncMock(return_value=[])
        mock_memory.return_value = mock_memory_instance

        mock_generate.return_value = "Привет! Как дела?"

        mock_update.message.text = "Привет!"

        await handle_message(mock_update, mock_context)

        mock_generate.assert_called_once()
        mock_update.message.reply_text.assert_called_once()

    @patch('app.bot.CharacterService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_reset_character(self, mock_session, mock_char_service, mock_update, mock_context, mock_character):
        """Тест сброса персонажа"""
        from app.bot import reset_character

        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=mock_character)
        mock_char_service.return_value = mock_char_instance

        await reset_character(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "удалить" in call_args
        assert mock_character.name in call_args

    @patch('app.bot.CharacterService')
    @patch('app.bot.MemoryService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_confirm_reset(self, mock_session, mock_memory, mock_char_service, mock_update, mock_context,
                                 mock_character):
        """Тест подтверждения сброса"""
        from app.bot import confirm_reset

        mock_context.user_data['reset_character_id'] = 1

        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=mock_character)
        mock_char_instance.delete_character = AsyncMock()
        mock_char_service.return_value = mock_char_instance

        mock_memory_instance = AsyncMock()
        mock_memory_instance.clear_all = AsyncMock()
        mock_memory.return_value = mock_memory_instance

        await confirm_reset(mock_update, mock_context)

        mock_memory_instance.clear_all.assert_called_once()
        mock_char_instance.delete_character.assert_called_once()
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "удалён" in call_args