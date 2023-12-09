from models import *

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



def see_work_schedule():
    pass

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



def see_zapys():
    pass


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


def add_service():

    with db:
        Service(title='стрижка', cost=100).save()

def add_master():

    with db:
        Master(name = 'Стефанія', specialty = 'перукар', experience = 2).save()

def add_serv_has_mstr():

    with db:
        Service_has_Master(service_id = 1, master_id = 1).save()

#see_services_and_prices()
#add_master()
#add_serv_has_mstr()