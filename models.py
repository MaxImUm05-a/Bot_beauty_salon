import peewee as pw

db = pw.SqliteDatabase('krasunya2.db')


class BaseModel(pw.Model):
    class Meta:
        database = db

class Master(BaseModel):
    """Майстер"""

    id_master = pw.AutoField()
    name = pw.TextField(null = False)
    specialty = pw.TextField(null = False)
    experience = pw.FloatField(null = False)

    class Meta:
        order_by = 'id_master'
        db_table = 'masters'


class Service(BaseModel):
    """Послуга"""

    id_service = pw.AutoField()
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

    id_client = pw.AutoField()
    phone_number = pw.TextField(null = False)
    name = pw.TextField(null = False)

    class Meta:
        order_by = 'id_client'
        db_table = 'clients'


class Booking(BaseModel):
    """Запис"""

    id_booking = pw.AutoField()
    date_time = pw.DateTimeField(null = False)

    client_id = pw.ForeignKeyField(Client, backref = 'bookings')
    master_id = pw.ForeignKeyField(Master, backref = 'bookings')
    service_id = pw.ForeignKeyField(Service, backref='bookings')

    class Meta:
        order_by = 'id_booking'
        db_table = 'bookings'


class Schedule(BaseModel):
    """Розклад роботи майстрів"""

    date = pw.DateField(null = False)
    # t08_09 = pw.ForeignKeyField(Booking)
    # t09_10 = pw.ForeignKeyField(Booking)
    # t10_11 = pw.ForeignKeyField(Booking)
    # t11_12 = pw.ForeignKeyField(Booking)
    # t12_13 = pw.ForeignKeyField(Booking)
    # t13_14 = pw.ForeignKeyField(Booking)
    # t14_15 = pw.ForeignKeyField(Booking)
    # t15_16 = pw.ForeignKeyField(Booking)
    # t16_17 = pw.ForeignKeyField(Booking)
    # t17_18 = pw.ForeignKeyField(Booking)
    # t18_19 = pw.ForeignKeyField(Booking)
    # t19_20 = pw.ForeignKeyField(Booking)
    t08_09 = pw.IntegerField(null=True)
    t09_10 = pw.IntegerField(null=True)
    t10_11 = pw.IntegerField(null=True)
    t11_12 = pw.IntegerField(null=True)
    t12_13 = pw.IntegerField(null=True)
    t13_14 = pw.IntegerField(null=True)
    t14_15 = pw.IntegerField(null=True)
    t15_16 = pw.IntegerField(null=True)
    t16_17 = pw.IntegerField(null=True)
    t17_18 = pw.IntegerField(null=True)
    t18_19 = pw.IntegerField(null=True)
    t19_20 = pw.IntegerField(null=True)
    master_id = pw.ForeignKeyField(Master, backref = 'schedules')

    class Meta:
        db_table = 'schedules'



def create_tables():
    with db:
        db.create_tables([Booking, Master, Client, Service, Service_has_Master])
        db.create_tables([Schedule])

#create_tables()