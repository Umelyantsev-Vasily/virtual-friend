from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class MenuKeyboard:
    """Клавиатуры для меню"""

    @staticmethod
    def main_menu(has_character: bool = False) -> ReplyKeyboardMarkup:
        """Главное меню - только базовые кнопки"""
        if not has_character:
            buttons = [
                [KeyboardButton("📝 Создать персонажа")],
            ]
        else:
            buttons = [
                [KeyboardButton("👤 Профиль")],
                [KeyboardButton("🔄 Сменить персонажа"), KeyboardButton("⚙️ Настройки")],
            ]

        return ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True,
            input_field_placeholder="Выберите действие..."
        )

    @staticmethod
    def cancel() -> ReplyKeyboardMarkup:
        """Кнопка отмены"""
        return ReplyKeyboardMarkup(
            [[KeyboardButton("❌ Отмена")]],
            resize_keyboard=True
        )

    @staticmethod
    def remove() -> ReplyKeyboardRemove:
        """Убрать клавиатуру"""
        return ReplyKeyboardRemove()