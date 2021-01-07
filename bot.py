from parserconf import get_token
from api import GetApi
from db import User
import telebot
import time
from keyboard import Keyboard, ReplyKeyboardRemove

bot = telebot.TeleBot(token=get_token())
DB = User()


@bot.message_handler(commands=["start"])
def start_bot(message):
    msg = bot.send_message(message.from_user.id, f"*Доброго времени суток {message.from_user.first_name}*",
                           parse_mode="Markdown",
                           reply_markup=Keyboard("Настройки", "Выдать котировки", resize_keyboard=True))
    bot.register_next_step_handler(msg, press_setting)


@bot.message_handler(regexp="setting")
def press_setting(message):
    if message.text == "Настройки":
        quots = DB.return_quotes(message.from_user.id)
        times = DB.return_time(message.from_user.id)
        if quots and times:
            args = [f"""----> """.join(x) for x in zip(quots, times)]
            msg = bot.send_message(message.from_user.id, f"*{message.from_user.first_name} ваши котировки и время "
                                                         f"отправления:\n "
                                                         f"{' | '.join(args)}*",
                                   parse_mode="Markdown",
                                   reply_markup=Keyboard("Добавить еще", "Сохранить", resize_keyboard=True))
            bot.register_next_step_handler(msg, add_more)
        else:
            msg = bot.send_message(message.from_user.id, f"*{message.from_user.first_name} у вас нет сохраненных"
                                                         f" котировок\n"
                                                         f"Введите 'Добавить'*",
                                   parse_mode="Markdown",
                                   reply_markup=ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, add_more)
    elif message.text == "Выдать котировки":
        quots = DB.return_quotes(message.from_user.id)
        if quots:
            for i in quots:
                _quots = i.split(" ")
                count = 1
                while count != len(_quots):
                    count += 1
                    api = GetApi(_quots[0], _quots[1])
                    bot.send_message(message.from_user.id, f'*{api.send_quotes()}*',
                                     parse_mode="Markdown",
                                     reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.from_user.id, f'*/start*', parse_mode='Markdown')

        else:
            bot.send_message(message.from_user.id,
                             f'*{message.from_user.first_name},к сожалению ваши данные не сохранены\n'
                             f'Для добавления данные введите /start,и нажмите Настройки*',
                             parse_mode="Markdown",
                             reply_markup=ReplyKeyboardRemove())

    else:
        bot.send_message(message.from_user.id, "*Что то пошло не так,попробуйте еще раз,"
                                               "введите команду /start*",
                         parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())


@bot.message_handler()
def add_more(message):
    if message.text == "Добавить еще" or message.text == "Добавить":
        bot.send_message(message.from_user.id,
                         f'*Окей {message.from_user.first_name},выбери время отправки,а так же валютную пару\n'
                         f'С понедельника по пятницу,я буду отправлять ваши котировки!*',
                         parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
        msg = bot.send_message(message.from_user.id, "*Введите время формата HH:MM \n "
                                                     "Например: 21:49*",
                               parse_mode="Markdown")
        bot.register_next_step_handler(msg, press_quotes)
    elif message.text == "Сохранить":
        bot.send_message(message.from_user.id,
                         f"*Окей,для начала работы введите /start*",
                         parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())

    else:
        bot.send_message(message.from_user.id, "*Что то пошло не так,попробуйте еще раз,"
                                               "введите команду /start*",
                         parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def press_quotes(message):
    try:
        quotes_ = GetApi()
        time.strptime(message.text, "%H:%M")
        DB.insert_db(message.from_user.id, message.from_user.first_name, message.text)
        bot.send_message(message.from_user.id,
                         "*Хорошо,со временем все отлично,осталось разобраться с валютной парой\n*",
                         parse_mode="Markdown")
        time.sleep(2)
        msg = bot.send_message(message.from_user.id, f"*Введите валютную пару формата: USD RUB\n"
                                                     "Данный пример покажет соотношение доллара к рублю\n"
                                                     f"Список валют:\n{quotes_.all_quotes()} *",
                               parse_mode="Markdown",
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, save_quotes)
    except ValueError:
        bot.send_message(message.from_user.id, "*Вы ввели неправильный формат времени,попробуйте еще раз,введите"
                                               "команду \n /start*",
                         parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda messages: True, content_types=["text"])
def save_quotes(message):
    texted_ = message.text.split(" ")
    quotes = GetApi(texted_[0], texted_[1])
    if texted_[0] in quotes.all_quotes() and texted_[1] in quotes.all_quotes():
        bot.send_message(message.from_user.id, f"* {quotes.send_quotes()}*",
                         parse_mode='Markdown')
        DB.update_db(message.text)
        bot.send_message(message.from_user.id, "*Сохранено!\n "
                                               "Для начала работы введите /start*",
                         parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id, "*Неправильная котировка валюты\n"
                                               "Введите команду /start,и повторите все сначало!*\n",
                         parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.polling()
