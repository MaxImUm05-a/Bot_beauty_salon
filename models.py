import peewee as pw

db = pw.SqliteDatabase('database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db

class Master(BaseModel):
    """Майстер"""

    id_master = pw.IntegerField(primary_key = True, null = False, unique = True)
    first_name = pw.TextField(null = False)
    middle_name = pw.TextField()
    last_name = pw.TextField(null = False)
    specialty = pw.TextField(null = False)
    experience = pw.FloatField(null = False)

    class Meta:
        order_by = 'id_master'
        db_table = 'masters'


class Service(BaseModel):
    """Послуга"""

    id_service = pw.IntegerField(primary_key = True, null = False, unique = True)
    title = pw.TextField(null = False)
    cost = pw.IntegerField(null = False)

    class Meta:
        order_by = 'id_service'
        db_table = 'services'


class Service_has_Master(BaseModel):
    """"Зв'язок багато до багатьох між Service та Master"""

    service_id = pw.ForeignKeyField(Service)
    master_id = pw.ForeignKeyField(Master)

    class Meta:
        db_table = 'services_have_masters'


class Client(BaseModel):
    """Клієнт"""

    id_client = pw.IntegerField(primary_key = True, null = False, unique = True)
    phone_number = pw.TextField(null = False)
    first_name = pw.TextField(null = False)
    middle_name = pw.TextField()
    last_name = pw.TextField(null = False)

    class Meta:
        order_by = 'id_client'
        db_table = 'clients'


class Booking(BaseModel):
    """Запис"""

    id_booking = pw.IntegerField(primary_key = True, null = False, unique = True)
    date_time = pw.DateTimeField(null = False)
    cost = pw.IntegerField(null = False)

    client_id = pw.ForeignKeyField(Client, backref = 'bookings')
    master_id = pw.ForeignKeyField(Master, backref = 'bookings')

    class Meta:
        order_by = 'id_booking'
        db_table = 'bookings'



def create_tables():
    with db:
        db.create_tables([Booking])

#create_tables()