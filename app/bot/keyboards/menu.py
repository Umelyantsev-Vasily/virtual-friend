from telegram import ReplyKeyboardMarkup, KeyboardButton


class MenuKeyboard:
    """Клавиатуры для меню"""

    @staticmethod
    def main_menu(has_character: bool = False) -> ReplyKeyboardMarkup:
        """Главное меню"""
        if not has_character:
            buttons = [
                [KeyboardButton("📝 Создать персонажа")],
                [KeyboardButton("ℹ️ О боте"), KeyboardButton("❓ Помощь")]
            ]
        else:
            buttons = [
                [KeyboardButton("💬 Диалог"), KeyboardButton("👤 Мой профиль")],
                [KeyboardButton("🔄 Сменить персонажа"), KeyboardButton("⚙️ Настройки")],
                [KeyboardButton("ℹ️ О боте"), KeyboardButton("❓ Помощь")]  # Добавим для удобства
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