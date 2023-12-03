import peewee as pw

db = pw.SqliteDatabase('database.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Service(BaseModel):
    """Послуга"""

    id_service = pw.IntegerField(primary_key = True, null = False, unique = True)
    title = pw.TextField(null = False)
    cost = pw.IntegerField(null = False)

    class Meta:
        order_by = 'id_service'
        db_table = 'services'


class Booking(BaseModel):
    """Запис"""

    id_booking = pw.IntegerField(primary_key = True, null = False, unique = True)
    date_time = pw.DateTimeField(null = False)
    cost = pw.IntegerField(null = False)

    class Meta:
        order_by = 'id_booking'
        db_table = 'bookoings'



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