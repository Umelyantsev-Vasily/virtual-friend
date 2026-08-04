import pytest
from app.bot.keyboards.menu import MenuKeyboard


class TestMenuKeyboard:
    """Тесты для клавиатур меню"""

    def test_main_menu_without_character(self):
        """Тест главного меню без персонажа"""
        keyboard = MenuKeyboard.main_menu(has_character=False)

        # Проверяем что клавиатура создана
        assert keyboard is not None
        assert keyboard.resize_keyboard is True

        # Проверяем кнопки
        buttons = keyboard.keyboard
        assert len(buttons) == 2  # Две строки

        # Первая строка
        assert buttons[0][0].text == "📝 Создать персонажа"

        # Вторая строка
        assert buttons[1][0].text == "ℹ️ О боте"
        assert buttons[1][1].text == "❓ Помощь"

    def test_main_menu_with_character(self):
        """Тест главного меню с персонажем"""
        keyboard = MenuKeyboard.main_menu(has_character=True)

        assert keyboard is not None
        assert keyboard.resize_keyboard is True

        buttons = keyboard.keyboard
        assert len(buttons) == 2

        # Первая строка
        assert buttons[0][0].text == "💬 Диалог"
        # Исправлено: "👤 Профиль" вместо "👤 Мой профиль"
        assert buttons[0][1].text == "👤 Профиль"

        # Вторая строка
        assert buttons[1][0].text == "🔄 Сменить персонажа"
        assert buttons[1][1].text == "⚙️ Настройки"

    def test_cancel_keyboard(self):
        """Тест клавиатуры отмены"""
        keyboard = MenuKeyboard.cancel()

        assert keyboard is not None
        assert keyboard.resize_keyboard is True

        buttons = keyboard.keyboard
        assert len(buttons) == 1
        assert buttons[0][0].text == "❌ Отмена"