from parserconf import get_token
from db import insert_db, check_data
import telebot
import time
from telebot import types
import requests
import re

bot = telebot.TeleBot(token=get_token())
time_list = []


def rexgex(text, rex):
    valid = re.findall(rex, text)
    if valid:
        return True
    else:
        return False


class GetApi:
    def __init__(self, base, symbols):
        self.api = "https://api.exchangeratesapi.io/latest"
        self.base = base
        self.symbols = symbols

    def send_quotes(self):
        quotes = None
        page = requests.get(self.api, params={
            'base': self.base,
            'symbols': self.symbols
        })
        if page.ok:
            page_ = page.json()['rates']
            for key, value in page_.items():
                quotes = f" {self.base} -> {self.symbols} {round(value, 2)}"
            return quotes
        else:
            return False

    def all_quotes(self):
        page = requests.get(self.api, params="rates")
        page_ = page.json()['rates']
        quotes = sorted([])
        for key in page_:
            quotes.append(key)
        return ', '.join(quotes)


def keyboard_start(a, b):
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_setting = types.KeyboardButton(a)
    button_quotes = types.KeyboardButton(b)
    keyboards.add(button_setting, button_quotes)

    return keyboards


@bot.message_handler(commands=["start"])
def start_bot(message):
    msg = bot.send_message(message.from_user.id, f"*Доброго времени суток {message.from_user.first_name}*",
                           parse_mode="Markdown",
                           reply_markup=keyboard_start("Настройки", "Выдать котировки"))
    bot.register_next_step_handler(msg, press_setting)


@bot.message_handler(func=lambda message: True)
def press_setting(message):
    if message.text == "Настройки":
        bot.send_message(message.from_user.id,
                         f'*Окей {message.from_user.first_name},выбери время отправки,а так же валютную пару\n'
                         f'С понедельника по пятницу,я буду отправлять ваши котировки!*',
                         parse_mode="Markdown",
                         reply_markup=types.ReplyKeyboardRemove())
        time.sleep(1)
        msg = bot.send_message(message.from_user.id, "*Введите время формата HH:MM \n "
                                                     "Например: 21:49*",
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, press_quotes)
    elif message.text == "Выдать котировки":
        a = check_data(message.from_user.id, "quotes")
        if a is not False:
            for i in a:
                times = i.split(" ")
                count = 1
                print(len(times))
                while count != len(times):
                    count += 1
                    api = GetApi(times[0], times[1])
                    bot.send_message(message.from_user.id, f'*{api.send_quotes()}*',
                                     parse_mode="Markdown",
                                     reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(message.from_user.id, f'*/start*', parse_mode='Markdown')

        else:
            bot.send_message(message.from_user.id,
                             f'*{message.from_user.first_name},к сожалению ваши данные не сохранены\n'
                             f'Для добавления данные введите /start,и нажмите Настройки*',
                             parse_mode="Markdown",
                             reply_markup=types.ReplyKeyboardRemove())

    else:
        bot.send_message(message.from_user.id, "*Что то пошло не так,попробуйте еще раз,"
                                               "введите команду /start*",
                         parse_mode="Markdown",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def press_quotes(message):
    if rexgex(message.text, r"[0-2]{1}[0-9]{1}\:[0-5]{1}[0-9]{1}"):

        msg = bot.send_message(message.from_user.id,
                               "*Хорошо,со временем все отлично,осталось разобраться с валютной парой\n*",
                               parse_mode="Markdown",
                               reply_markup=keyboard_start("Добавить еще", "Сохранить"))

        bot.register_next_step_handler(msg, add_save)

        return time_list.append(message.text)
    else:
        bot.send_message(message.from_user.id, "*Вы ввели неправильный формат времени,попробуйте еще раз,введите"
                                               "команду \n /start*",
                         parse_mode="Markdown",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True, content_types=["text"])
def add_save(message):
    if message.text == "Добавить еще":

        msg = bot.send_message(message.from_user.id, "*Введите валютную пару формата: USD RUB\n"
                                                     "Данный пример покажет соотношение доллара к рублю\n"
                                                     "Посмотреть валютные пары можно командой /quotes*\n",
                               parse_mode="Markdown",
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, save_quotes)

    elif message.text == "Сохранить":
        bot.send_message(message.from_user.id, "Сохранено!\n "
                                               "Для начала работы введите /start")
    else:
        bot.send_message(message.from_user.id, "Что то пошло не так,попробуйте еще раз,введите"
                                               "команду /start",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True, content_types=["text"])
def save_quotes(message):
    if rexgex(message.text, r"[A-Z]{3}\s[A-Z]{3}"):
        texted_ = message.text.split(" ")
        quotes = GetApi(texted_[0], texted_[1])
        if quotes.send_quotes() is not False:
            bot.send_message(message.from_user.id, f"* {quotes.send_quotes()}*",
                             parse_mode='Markdown')
            insert_db(int(message.from_user.id), message.from_user.first_name, message.text, "".join(time_list))
            print(time_list)
            if len(time_list) >= 1:
                time_list.clear()

            bot.send_message(message.from_user.id, "*Сохранено!\n "
                                                   "Для начала работы введите /start*",
                             parse_mode='Markdown')
        else:
            bot.send_message(message.from_user.id, "*Неправильная котировка валюты\n"
                                                   "Введите команду /start,и повторите все сначало!*\n",
                             parse_mode="Markdown",
                             reply_markup=types.ReplyKeyboardRemove())

    elif message.text == "/quotes":
        quotes__ = GetApi(None, None)
        bot.send_message(message.from_user.id, f"*Список валют: {quotes__.all_quotes()}\n"
                                               f"/start*",

                         parse_mode="Markdown",
                         reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, "*Неправильная котировка валюты\n"
                                               "Введите команду /start,и повторите все сначало!*\n",
                         parse_mode="Markdown",
                         reply_markup=types.ReplyKeyboardRemove())


bot.polling()
