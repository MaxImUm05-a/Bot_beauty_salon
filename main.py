import telebot as t
from telebot import types
import data_base as dat
import datetime as dtm

TOKEN = '5758066916:AAHC3IZWJkvq7V9BUBolfCzO94PoYH5pKdM'
bot = t.TeleBot(TOKEN)

info = []
info_msg = []


def create_menu_button():
    """Створення клавіатури, яка містить кнопку для повернення в меню"""

    kb = types.ReplyKeyboardMarkup(one_time_keyboard = False)
    menu_btn = types.KeyboardButton(text = 'Повернутись в меню')
    kb.add(menu_btn)

    return kb




def delete_msg(info, chat_id, message_id):
    """Видалення повідомлення"""

    for i in info:
        if chat_id == i[0]:
            bot.delete_message(i[0], i[1])
            bot.delete_message(chat_id, message_id)
            del info[info.index(i)]
            return info


@bot.message_handler(commands=['start'])
def start(message):
    global info_msg

    kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    time_work = types.KeyboardButton(text = 'Перегляд часу роботи')
    see_serv = types.KeyboardButton(text = 'Перегляд послуг')
    see_master = types.KeyboardButton(text = 'Перегляд майстрів')
    see_my_book = types.KeyboardButton(text = 'Перегляд мого запису')
    kb.add(time_work, see_serv, see_master, see_my_book)

    msg = bot.send_message(message.chat.id, 'Що ви хочете зробити?', reply_markup=kb)

    info_msg.append([])
    info_msg[-1].append(message.chat.id)
    info_msg[-1].append(msg.message_id)


@bot.message_handler(content_types = ['text'])
def get_text(message):
    global info_msg


    match message.text:
        case 'Перегляд часу роботи':
            info_msg = delete_msg(info_msg, message.chat.id, message.message_id)

            bot.send_message(message.chat.id, 'Ми працюємо\nПн-Пт  з 8:00 до 20:00\nСб-Нд  вихідний', reply_markup = create_menu_button())

        case 'Перегляд послуг':
            serv_price = dat.see_services_and_prices()

            kb = types.InlineKeyboardMarkup(row_width=2)

            btn = []
            mes = 'Ось наші послуги, які ми можемо вам запропонувати:\n'

            for sp in serv_price:
                btn.append(
                    types.InlineKeyboardButton(text=sp[1], callback_data='serv' + str(sp[0])))
                mes = mes + sp[1] + '  ---  ' + 'ціна: ' + str(sp[2]) + '\n'

            for rah in range(len(btn)):
                kb.add(btn[rah])


            info_msg = delete_msg(info_msg, message.chat.id, message.message_id)

            msg = bot.send_message(message.chat.id, mes, reply_markup=kb)

            info_msg.append([])
            info_msg[-1].append(message.chat.id)
            info_msg[-1].append(msg.message_id)

        case 'Перегляд майстрів':
            masters = dat.see_masters()
            print(masters)

            kb = types.InlineKeyboardMarkup(row_width=2)

            btn = []
            for mt in masters:
                btn.append(types.InlineKeyboardButton(
                    text='Ім\'я: ' + mt[1] + ' Спеціальність: ' + str(mt[2]) + ' Досвід: ' + '%s р.' % mt[3],
                    callback_data='mast' + str(mt[0])))

            for rah in range(len(btn)):
                kb.add(btn[rah])

            info_msg = delete_msg(info_msg, message.chat.id, message.message_id)

            msg = bot.send_message(message.chat.id, 'Ось наші майстри:', reply_markup=kb)

            info_msg.append([])
            info_msg[-1].append(message.chat.id)
            info_msg[-1].append(msg.message_id)

        case 'Перегляд мого запису':
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            reg_button = types.KeyboardButton(text="Поділитись номером телефону", request_contact=True)
            keyboard.add(reg_button)
            response = bot.send_message(message.chat.id,
                                        "Поділись своїм номер телефону, будь ласка",
                                        reply_markup=keyboard)

            info_msg = delete_msg(info_msg, message.chat.id, message.message_id)

            msg = bot.register_next_step_handler(response, next_view)

            info_msg.append([])
            info_msg[-1].append(message.chat.id)
            info_msg[-1].append(msg.message_id)

        case 'Повернутись в меню':
            kb = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            time_work = types.KeyboardButton(text='Перегляд часу роботи')
            see_serv = types.KeyboardButton(text='Перегляд послуг')
            see_master = types.KeyboardButton(text='Перегляд майстрів')
            see_my_book = types.KeyboardButton(text='Перегляд мого запису')
            kb.add(time_work, see_serv, see_master, see_my_book)

            msg = bot.send_message(message.chat.id, 'Що ви хочете зробити?', reply_markup=kb)

            info_msg.append([])
            info_msg[-1].append(message.chat.id)
            info_msg[-1].append(msg.message_id)

        case _:
            pass





def next_view(message):
    try:
        client_id = dat.get_client_id(message.contact.phone_number)
        info = dat.get_booking(client_id)
        master_info = dat.get_masters_from_master(info[1])
        service_info = dat.get_services_from_service(info[2])

        date = info[0].strftime('%d.%m.%Y')
        time = info[0].strftime('%H:%M')

        msg = f'Ось інформація про ваш запис:\nДата: {date}\nЧас на котру потрібно підійти: {time}\nІм\'я вашого майстра: ' \
              f'{master_info[1]}\nПослуга, за якою ви звертаєтесь до нас: {service_info[1]}\nЦіна: {service_info[2]}грн'

        bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, 'У вас немає запису')


@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if 'serv' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)

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
                callback_data='book ' + str(serv_id) + ' ' + str(mt[0])))
        for rah in range(len(btn)):
            kb.add(btn[rah])

        bot.send_message(call.message.chat.id, 'Ось наші майстри, які пропонують цю послугу:', reply_markup=kb)

    if 'mast' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        mast_id = int(call.data[4:])
        services_id = dat.get_services_from_mast(mast_id)
        services = []
        for service_id in services_id:
            services.append(dat.get_services_from_service(service_id))

        kb = types.InlineKeyboardMarkup(row_width=3)
        btn = []
        for sv in services:
            btn.append(types.InlineKeyboardButton(text = sv[1]+'\n'+'Ціна: '+str(sv[2]), callback_data = 'book '+str(sv[0]) +' '+ str(mast_id)))
        for rah in range(len(btn)):
            kb.add(btn[rah])

        bot.send_message(call.message.chat.id, 'Ось послуги, які пропонує цей майстер', reply_markup=kb)

    if 'book' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        serv_mast = call.data.split(' ')
        service_id = serv_mast[1]
        master_id = serv_mast[2]
        may_to_book = dat.get_schedule_of_master(master_id)

        kb = types.InlineKeyboardMarkup(row_width=4)
        days = []
        btn = []
        for day in may_to_book:
            if isinstance(day, str):
                btn.append(types.InlineKeyboardButton(text = day, callback_data = 'booday' + ' ' + day + ' ' + service_id +
                                                      ' ' + master_id))
                days.append(day)

        for x in range(len(btn)):
            kb.add(btn[x])

        msg = 'Ось дні і години на які ви можете записатись до цього майстра:\n'
        mes = []
        for day in may_to_book:
            if isinstance(day, dict):
                mes.append(list(day.keys()))

        for x in range(len(days)):
            msg = msg + days[x] + ' -- '
            for y in range(len(mes[x])):
                msg = msg + mes[x][y] + ' '
            msg = msg + '\n'

        bot.send_message(call.message.chat.id, msg, reply_markup = kb)

    if 'booday' in call.data:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        serv_mast = call.data.split(' ')
        day = serv_mast[1]
        service_id = serv_mast[2]
        master_id = serv_mast[3]
        may_to_book = dat.get_schedule_of_master(master_id)
        day_may = may_to_book.index(day)
        hours = list(may_to_book[day_may+1].keys())

        kb = types.InlineKeyboardMarkup(row_width = 4)
        btn = []
        for hour in hours:
            btn.append(types.InlineKeyboardButton(text = hour, callback_data = 'boohour' + ' ' + hour + ' ' + day + ' '
                                                                               + service_id + ' ' + master_id))
        for x in range(len(btn)):
            kb.add(btn[x])

        bot.send_message(call.message.chat.id, 'Виберіть на котру годину вам найкраще підійти', reply_markup = kb)

    if 'boohour' in call.data:
        global info
        bot.delete_message(call.message.chat.id, call.message.message_id)

        user_id = call.message.chat.id
        info.append(user_id)
        info.append([])
        serv_mast = call.data.split(' ')
        hour = serv_mast[1]
        day = serv_mast[2]
        service_id = serv_mast[3]
        master_id = serv_mast[4]
        time = hour[:5]
        dt = day + ' ' + time
        date_time = dtm.datetime.strptime(dt, '%d.%m.%Y %H:%M')

        info[-1].append(date_time)
        info[-1].append(service_id)
        info[-1].append(master_id)


        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        reg_button = types.KeyboardButton(text="Поділитись номером телефону", request_contact=True)
        keyboard.add(reg_button)
        response = bot.send_message(call.message.chat.id,
                                    "Поділись своїм номер телефону, будь ласка",
                                    reply_markup=keyboard)
        bot.register_next_step_handler(response, next_zapys)


def next_zapys(message):
    global info

    dat.add_client(message.contact.phone_number, message.contact.first_name)
    client_id = dat.get_client_id(message.contact.phone_number)

    user_id = message.chat.id
    for i in info:
        if isinstance(i, int):
            if i == user_id:
                dat.add_booking(info[info.index(i)+1][0], info[info.index(i)+1][1], info[info.index(i)+1][2], client_id)

                booking_id = dat.get_booking(client_id, 1)
                date_time = info[info.index(i) + 1][0]
                schedule_id = dat.get_schedule(date_time, info[info.index(i)+1][2])
                hour = date_time.strftime('%H')
                dat.change_schedule(hour, booking_id, schedule_id)

                bot.send_message(message.chat.id, 'Ви зробили запис!', reply_markup = create_menu_button())




bot.infinity_polling()