from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


class Keyboard(ReplyKeyboardMarkup):
    def __init__(self, a, b, resize_keyboard=None):
        super(Keyboard, self).__init__(resize_keyboard=None)
        self.resize_keyboard = resize_keyboard
        self.a = a
        print(type(a))
        self.b = b
        print(type(b))
        self.add(KeyboardButton(self.a), KeyboardButton(self.b))
