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




def add_service():

    with db:
        Service(title='стрижка', cost=100).save()

def add_master():

    with db:
        Master(name = 'Стефанія', specialty = 'перукар', experience = 2).save()


#see_services_and_prices()
#add_master()