import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.bot.keyboards.menu import MenuKeyboard


@pytest.mark.asyncio
class TestFullIntegration:
    """Полные интеграционные тесты"""

    @patch('app.bot.CharacterService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_full_character_creation_flow(self, mock_session, mock_char_service, mock_update, mock_context):
        """Тест полного потока создания персонажа"""
        from app.bot import new_character, handle_character_creation

        # Шаг 1: Начать создание
        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=None)
        mock_char_service.return_value = mock_char_instance

        await new_character(mock_update, mock_context)

        assert mock_context.user_data.get('creating_character') is True

        # Шаг 2: Ввести имя
        mock_update.message.text = "TestFriend"
        await handle_character_creation(mock_update, mock_context)
        assert mock_context.user_data['character_name'] == "TestFriend"

        # Шаг 3: Ввести возраст
        mock_update.message.text = "25"
        await handle_character_creation(mock_update, mock_context)
        assert mock_context.user_data['character_age'] == 25

        # Шаг 4: Ввести пол
        mock_update.message.text = "Мужской"
        await handle_character_creation(mock_update, mock_context)
        assert mock_context.user_data['character_gender'] == "Мужской"

        # Шаг 5: Ввести характер
        mock_char_instance.create_custom_character = AsyncMock(return_value=MagicMock(
            name="TestFriend",
            age=25,
            gender="Мужской",
            personality="Дружелюбный"
        ))

        mock_update.message.text = "Дружелюбный"
        await handle_character_creation(mock_update, mock_context)

        # Проверяем что данные очищены
        assert mock_context.user_data.get('creating_character') is None

    def test_menu_flow(self):
        """Тест потока меню"""
        # Проверяем что меню переключается
        menu_without = MenuKeyboard.main_menu(False)
        menu_with = MenuKeyboard.main_menu(True)

        # Меню без персонажа имеет кнопку создания
        has_create = any(
            any(btn.text == "📝 Создать персонажа" for btn in row)
            for row in menu_without.keyboard
        )
        assert has_create is True

        # Меню с персонажем имеет кнопку диалога
        has_dialog = any(
            any(btn.text == "💬 Диалог" for btn in row)
            for row in menu_with.keyboard
        )
        assert has_dialog is True

        # Меню с персонажем НЕ имеет кнопки создания
        has_create_with = any(
            any(btn.text == "📝 Создать персонажа" for btn in row)
            for row in menu_with.keyboard
        )
        assert has_create_with is False

    @patch('app.bot.CharacterService')
    @patch('app.bot.AsyncSessionLocal')
    async def test_cancel_creation_flow(self, mock_session, mock_char_service, mock_update, mock_context):
        """Тест отмены создания персонажа"""
        from app.bot import handle_message

        # Настраиваем состояние создания
        mock_context.user_data['creating_character'] = True
        mock_context.user_data['character_name'] = "TestFriend"

        mock_char_instance = AsyncMock()
        mock_char_instance.get_by_user_id = AsyncMock(return_value=None)
        mock_char_service.return_value = mock_char_instance

        mock_update.message.text = "❌ Отмена"

        await handle_message(mock_update, mock_context)

        # Проверяем что данные очищены
        assert mock_context.user_data.get('creating_character') is None
        assert mock_context.user_data.get('character_name') is None

        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args[0][0]
        assert "отменено" in call_args