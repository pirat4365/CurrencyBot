from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


class Keyboard(ReplyKeyboardMarkup):
    def __init__(self, a, b, resize_keyboard=None):
        super(Keyboard, self).__init__(resize_keyboard=None)
        self.resize_keyboard = resize_keyboard
        self.a = a
        self.b = b
        self.add(KeyboardButton(self.a), KeyboardButton(self.b))
