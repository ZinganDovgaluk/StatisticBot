import telebot
from classes import config
from classes.Users import Users
from classes.Tools import BackTool
from classes.Community import Groups
from telebot import types
from time import sleep, time, ctime
from threading import Thread
import schedule
from classes.storage import Loader
from classes.TimeStruct import Time


# Thread begin


def send_lesson():
    users = Loader.load_data()
    for user_id in users:
        if users[user_id]["remind"] is True:
            group = Groups.get_group_by_group_name(Users.get_group_by_user_id(user_id))
            today = group.get_day(BackTool.get_time_dict()["day"])
            for lesson in today.lessons:
                if lesson.time_period.begin.get_str() == BackTool.get_curr_time_str(add_min=3):
                    bot.send_message(user_id, "<b>Нагадую, через 3 хвилини розпочинається пара:</b>", parse_mode='html')
                    bot.send_message(user_id, lesson.get_info())
                    try:
                        print("Message sent to " + str(user_id))
                    except:
                        print("Error")


schedule.every().day.at("12:07").do(send_lesson)
schedule.every().day.at("13:37").do(send_lesson)
schedule.every().day.at("15:07").do(send_lesson)
schedule.every().day.at("16:37").do(send_lesson)
schedule.every().day.at("18:07").do(send_lesson)


def message_reminder():
    while True:
        schedule.run_pending()
        sleep(5)


bot = telebot.TeleBot(config.TOKEN)
Thread(target=message_reminder).start()


# Thread end


@bot.message_handler(commands=['start'])
def welcome(message):
    Users.authorize(user_id=message.chat.id, user_group="ipz21/1")
    bot.send_message(message.chat.id,
                     "Привіт, {0.first_name}!\nЯ - <b>{1.first_name}</b>."
                     " Мене було створено, щоб допомогти вам відстежувати "
                     "свій розклад.\n".format(message.from_user, bot.get_me()),
                     parse_mode='html')

    set_group(message)


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     "<b>Список команд:</b>\n"
                     "/info - вивести список команд\n"
                     "/start - запустити бота\n"
                     "/group - змінити групу\n"
                     "/remind - увімкнути сповіщення\n"
                     "/now - вивести поточну пару\n"
                     "/today - вивести сьогоднішні пари\n"
                     "/week - вивести пари на всю неділю"
                     .format(message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(commands=['group'])
def set_group(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button211 = types.InlineKeyboardButton("ІПЗ-21/1", callback_data="ipz21/1")
    button212 = types.InlineKeyboardButton("ІПЗ-21/2", callback_data="ipz21/2")
    markup.add(button211, button212)

    bot.send_message(message.chat.id,
                     "Будь-ласка, оберіть свою групу.".format(message.from_user, bot.get_me()),
                     reply_markup=markup)


@bot.message_handler(commands=['today'])
def today(message):
    group = Groups.get_group_by_group_name(Users.get_group_by_user_id(message.chat.id))
    today = group.get_day(BackTool.get_time_dict()["day"])
    for lesson in today.lessons:
        bot.send_message(message.chat.id, lesson.get_info())


@bot.message_handler(commands=['now'])
def now(message):
    group = Groups.get_group_by_group_name(Users.get_group_by_user_id(message.chat.id))
    today = group.get_day(BackTool.get_time_dict()["day"])
    flag = False
    for lesson in today.lessons:
        now = BackTool.get_time_dict()
        if BackTool.is_between(lesson.time_period.begin.to_seconds(),
                               Time(now['hours'], now['minutes'], now['seconds']).to_seconds(),
                               lesson.time_period.end.to_seconds()):
            bot.send_message(message.chat.id, lesson.get_info())
            flag = True

    if flag is False:
        bot.send_message(message.chat.id, "Поточної пари не знайдено!")


@bot.message_handler(commands=['week'])
def week(message):
    group = Groups.get_group_by_group_name(Users.get_group_by_user_id(message.chat.id))
    week = group.week
    for day in week.days.values():
        bot.send_message(message.chat.id, day.get_info(),parse_mode='html')


@bot.message_handler(commands=['remind'])
def reminder(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton("Так", callback_data="Так")
    button_no = types.InlineKeyboardButton("Ні", callback_data="Ні")
    markup.add(button_yes, button_no)

    persons = Loader.load_data()
    if persons[str(message.chat.id)]["remind"] is True:
        bot.send_message(message.chat.id, "Нагадувач працює. Ви хотіли б його вимкнути?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Нагадувач вимкнено. Ти хотіли б його ввімкнути?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message.text == "Будь-ласка, оберіть свою групу.":
        group = call.data
        # Remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Ти обрав групу.", reply_markup=None)
        # Add user to base
        Users.authorize(user_id=call.message.chat.id, user_group=group)
        info(call.message)

    elif call.message.text == "Нагадувач працює. Ви хотіли б його вимкнути?":
        answer = call.data
        if answer == "Так":
            Users.switch_off_remind_by_user_id(call.message.chat.id)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач вимкнено.", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач працює.", reply_markup=None)

    elif call.message.text == "Нагадувач вимкнено. Ти хотіли б його ввімкнути?":
        answer = call.data
        if answer == "Так":
            Users.switch_on_remind_by_user_id(call.message.chat.id)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач увімкнено.", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Нагадувач вимкнений.", reply_markup=None)


@bot.message_handler(content_types=['text'])
def reaction(message):
    info(message)


# RUN
bot.polling(none_stop=True, interval=1)
