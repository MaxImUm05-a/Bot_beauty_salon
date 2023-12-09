import telebot as t
from telebot import types
import data_base as dat

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


@bot.message_handler(content_types = ['text'])
def get_text(message):
    if message.text == 'Перегляд часу роботи':
        bot.send_message(message.chat.id, 'Ми працюємо\nПн-Пт  з 8:00 до 20:00\nСб-Нд  вихідний')
    elif message.text == 'Перегляд послуг':
        serv_price = dat.see_services_and_prices()

        kb = types.InlineKeyboardMarkup(row_width=2)

        btn = []
        for sp in serv_price:
            btn.append(types.InlineKeyboardButton(text = sp[1]+'\n'+'Ціна: '+str(sp[2]), callback_data = 'serv'+str(sp[0])))

        for rah in range(len(btn)):
            kb.add(btn[rah])

        msg = bot.send_message(message.chat.id, 'Ось наші послуги, які ми можемо вам запропонувати', reply_markup = kb)

    elif message.text == 'Перегляд майстрів':
        masters = dat.see_masters()
        print(masters)

        kb = types.InlineKeyboardMarkup(row_width=2)

        btn = []
        for mt in masters:
            btn.append(types.InlineKeyboardButton(text='Ім\'я: '+mt[1] + ' Спеціальність: ' + str(mt[2]) + ' Досвід: ' + '%s р.' % mt[3],
                                                  callback_data='mast' + str(mt[0])))

        for rah in range(len(btn)):
            kb.add(btn[rah])

        bot.send_message(message.chat.id, 'Ось наші майстри:', reply_markup=kb)


@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if 'serv' in call.data:
        serv_id = int(call.data[4:])
        masters_id = dat.get_masters_from_serv(serv_id)
        masters = []
        for master_id in masters_id:
            masters.append(dat.get_masters_from_master(master_id))

        kb = types.InlineKeyboardMarkup(row_width=3)
        btn = []
        for mt in masters:
            btn.append(types.InlineKeyboardButton(
                text='Ім\'я: ' + mt[1] + ' Спеціальність: ' + str(mt[2]) + ' Досвід: ' + '%s р.' % mt[3],
                callback_data='ms_book' + str(mt[0])))         #ще потрібно зберігати послугу
        for rah in range(len(btn)):
            kb.add(btn[rah])

        bot.send_message(call.message.chat.id, 'Ось наші майстри, які пропонують цю послугу:', reply_markup=kb)

    if 'mast' in call.data:
        print('done')
        mast_id = int(call.data[4:])
        services_id = dat.get_services_from_mast(mast_id)
        services = []
        for service_id in services_id:
            services.append(dat.get_services_from_service(service_id))

        kb = types.InlineKeyboardMarkup(row_width=3)
        btn = []
        for sv in services:
            btn.append(types.InlineKeyboardButton(text = sv[1]+'\n'+'Ціна: '+str(sv[2]), callback_data = 'sv_book'+str(sv[0])))
        for rah in range(len(btn)):
            kb.add(btn[rah])

        bot.send_message(call.message.chat.id, 'Ось послуги, які пропонує цей майстер', reply_markup=kb)


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