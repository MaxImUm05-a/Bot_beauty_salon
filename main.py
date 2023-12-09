import telebot as t
from telebot import types

TOKEN = '5758066916:AAHC3IZWJkvq7V9BUBolfCzO94PoYH5pKdM'
bot = t.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup()
    time_work = types.KeyboardButton(text = 'Перегляд часу роботи')
    see_serv = types.KeyboardButton(text = 'Перегляд послуг')
    see_master = types.KeyboardButton(text = 'Перегляд майстрів')
    kb.add(time_work, see_serv, see_master)

    msg = bot.send_message(message.chat.id, 'Що ви хочете зробити?', reply_markup=kb)



@bot.message_handler(commands=['zapys'])
def zapys(message):
    """Запис до салону краси"""

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="Поділитись номером телефону", request_contact=True)
    keyboard.add(reg_button)
    response = bot.send_message(message.chat.id,
                                "Поділись своїм номер телефону, будь ласка",
                                reply_markup=keyboard)
    bot.register_next_step_handler(response, next_zapys)

def next_zapys(message):
    print(message.contact.phone_number, message.contact.first_name)


@bot.message_handler(commands = ['price'])
def see_service(message):
    """Подивитися послуги і ціни на їх"""

    pass



bot.infinity_polling()