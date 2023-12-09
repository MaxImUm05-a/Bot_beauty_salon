from models import *

def see_services_and_prices():
    """Подивитися послуги і ціни на їх"""

    query = (Service
             .select(Service, Master)
             .join(Service_has_Master)
             .join(Master)
             .where(Service.title == 'стрижка'))

    print('done')

    for q in query:
        print(q)



def see_work_schedule():
    pass

def zapys():
    """Запис клієнта"""

    with db:
        pass

def see_masters():
    pass

def see_zapys():
    pass




def add_service():

    with db:
        Service(title='стрижка', cost=100).save()


see_services_and_prices()