# tests/conftest.py
import pytest
from unittest.mock import MagicMock, AsyncMock
from telegram import Update, User, Message


@pytest.fixture
def mock_update():
    """Создает мок объекта Update"""
    update = MagicMock(spec=Update)
    update.effective_user = MagicMock()
    update.effective_user.id = 123456789
    update.effective_user.first_name = "TestUser"
    update.effective_user.username = "test_user"

    update.message = MagicMock()
    update.message.text = "Test message"
    update.message.reply_text = AsyncMock()

    return update


@pytest.fixture
def mock_context():
    """Создает мок объекта Context"""
    context = MagicMock()
    context.user_data = {}
    context.bot = MagicMock()
    context.bot.send_message = AsyncMock()
    return context


@pytest.fixture
def mock_character():
    """Создает мок персонажа"""
    character = MagicMock()
    character.id = 1
    character.name = "TestFriend"
    character.age = 25
    character.gender = "Мужской"
    character.personality = "Дружелюбный, веселый"
    character.is_active = True
    return character