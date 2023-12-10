from models import *
import datetime as dt

def see_services_and_prices():
    """Подивитися послуги і ціни на їх"""

    with db:
        serv_price = []

        servs = Service.select()

        for serv in servs:
            serv_price.append([])
            serv_price[-1].append(serv.id_service)
            serv_price[-1].append(serv.title)
            serv_price[-1].append(serv.cost)

    return serv_price


def zapys():
    """Запис клієнта"""

    with db:
        pass

def see_masters():
    """Подивитися майстрів"""

    with db:
        mstrs = []

        masters = Master.select()

        for master in masters:
            mstrs.append([])
            mstrs[-1].append(master.id_master)
            mstrs[-1].append(master.name)
            mstrs[-1].append(master.specialty)
            mstrs[-1].append(master.experience)

    return mstrs



def get_booking(client_id, need_id = 0):
    """Отримати інформацію про запис"""

    with db:
        info = []

        bookings = Booking.select().where(Booking.client_id == client_id)

        for booking in bookings:
            info.append(booking.date_time)
            info.append(booking.master_id)
            info.append(booking.service_id)
            id = booking.id_booking

    if need_id == 0:
        return info
    else:
        return id


def get_masters_from_serv(serv_id):
    """Отримати всіх майстрів з вказаною послугою"""

    with db:
        mstrs = []

        masters = Service_has_Master.select().where(Service_has_Master.service_id == serv_id)

        for master in masters:
            mstrs.append(master.master_id)

    return mstrs


def get_masters_from_master(master_id):
    """Отримати всю інфу про майстра з його айді"""

    with db:
        mstrs = []

        masters = Master.select().where(Master.id_master == master_id)

        for master in masters:
            mstrs.append(master.id_master)
            mstrs.append(master.name)
            mstrs.append(master.specialty)
            mstrs.append(master.experience)

    return mstrs



def get_services_from_mast(mast_id):
    """Отримати всі послуги з вказаного майстра"""

    with db:
        servs = []

        services = Service_has_Master.select().where(Service_has_Master.master_id == mast_id)

        for service in services:
            servs.append(service.service_id)

    return servs


def get_services_from_service(service_id):
    """Отримати всю інфу про послугу з послуг"""

    with db:
        servs = []

        services = Service.select().where(Service.id_service == service_id)

        for service in services:
            servs.append(service.id_service)
            servs.append(service.title)
            servs.append(service.cost)

    return servs


def perevirk_schedule(time):
    """Перевіряє стан часу з розкладу"""

    if time == 0:
        return True
    else:
        return False


def perevir_unique_clients(phone_number):

    with db:

        try:
            clients = Client.select().where(Client.phone_number == phone_number)
            for client in clients:
                if client.phone_number == phone_number:
                    return True
        except:
            return False


def get_schedule_of_master(master_id):
    """Отримати час, на який можна записатись"""

    with db:
        may_to_book = []

        days = Schedule.select().where(Schedule.master_id == master_id)

        for day in days:
            may_to_book.append(day.date.strftime('%d.%m.%Y'))
            may_to_book.append({})
            if perevirk_schedule(day.t08_09):
                may_to_book[-1]['08:00-09:00'] = True
            if perevirk_schedule(day.t09_10):
                may_to_book[-1]['09:00-10:00'] = True
            if perevirk_schedule(day.t10_11):
                may_to_book[-1]['10:00-11:00'] = True
            if perevirk_schedule(day.t11_12):
                may_to_book[-1]['11:00-12:00'] = True
            if perevirk_schedule(day.t12_13):
                may_to_book[-1]['12:00-13:00'] = True
            if perevirk_schedule(day.t13_14):
                may_to_book[-1]['13:00-14:00'] = True
            if perevirk_schedule(day.t14_15):
                may_to_book[-1]['14:00-15:00'] = True
            if perevirk_schedule(day.t15_16):
                may_to_book[-1]['15:00-16:00'] = True
            if perevirk_schedule(day.t16_17):
                may_to_book[-1]['16:00-17:00'] = True
            if perevirk_schedule(day.t17_18):
                may_to_book[-1]['17:00-18:00'] = True
            if perevirk_schedule(day.t18_19):
                may_to_book[-1]['18:00-19:00'] = True
            if perevirk_schedule(day.t19_20):
                may_to_book[-1]['19:00-20:00'] = True

    return may_to_book


def change_schedule(hour, booking_id, schedule_id):
    with db:
        if hour == '8':
            Schedule.update({Schedule.t08_09:booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '9':
            Schedule.update({Schedule.t09_10: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '10':
            Schedule.update({Schedule.t10_11: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '11':
            Schedule.update({Schedule.t11_12: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '12':
            Schedule.update({Schedule.t12_13: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '13':
            Schedule.update({Schedule.t13_14: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '14':
            Schedule.update({Schedule.t14_15: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '15':
            Schedule.update({Schedule.t15_16: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '16':
            Schedule.update({Schedule.t16_17: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '17':
            Schedule.update({Schedule.t17_18: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '18':
            Schedule.update({Schedule.t18_19: booking_id}).where(Schedule.id == schedule_id).execute()
        elif hour == '19':
            Schedule.update({Schedule.t19_20: booking_id}).where(Schedule.id == schedule_id).execute()


def get_schedule(date, master_id):
    with db:
        schedules = Schedule.select().where(Schedule.master_id == master_id, Schedule.date == date)

        for schedule in schedules:
            return schedule.id


def add_booking(date_time, service_id, master_id, client_id):
    """Створення замовлення"""

    with db:
        Booking(date_time = date_time, service_id = service_id, client_id = client_id, master_id = master_id).save()



def add_client(phone_number, name):
    """Створення слієнта"""

    with db:
        if perevir_unique_clients(phone_number) == False:
            Client(phone_number=phone_number, name=name).save()


def get_client_id(phone_number):
    """Отримати client_id"""

    with db:
        clients = Client.select().where(Client.phone_number == phone_number)

        for client in clients:
            client_id = client.id_client

    return client_id


def add_service():

    with db:
        Service(title='стрижка', cost=100).save()

def add_master():

    with db:
        Master(name = 'Стефанія', specialty = 'перукар', experience = 2).save()

def add_serv_has_mstr():

    with db:
        Service_has_Master(service_id = 1, master_id = 1).save()


def add_schedule():

    with db:
        Schedule(master_id = 1, date = dt.date(year = 2024, month = 2, day = 14), t08_09 = None, t09_10 = None, t10_11 = None, t11_12 = 0, t12_13 = 0,
                 t13_14 = 0, t14_15 = None, t15_16 = 0, t16_17 = 0, t17_18 = 0, t18_19 = None, t19_20 = None).save()

# see_services_and_prices()
# add_service()
# add_master()
# add_serv_has_mstr()
# add_schedule()