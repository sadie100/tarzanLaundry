from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.laundryDB

from datetime import datetime, date, timedelta
import random

today = date.today()
tomorrow = (datetime(today.year,today.month,today.day) + timedelta(days=1))

fieldArray=[]
for time in range(6,24):
    fieldArray.append({
        'date' : datetime(today.year,today.month,today.day,time),
        'user':f'user{time}',
        'type': random.choice(['laundry','dry']),
        'room': random.choice(['325','326']),
        'certification' : True
    })

tomorrowArray=[]
for time in range(6,24):
    tomorrowArray.append({
        'date' : datetime(tomorrow.year,tomorrow.month,tomorrow.day,time),
        'user':f'user{time}',
        'type': random.choice(['laundry','dry']),
        'room': random.choice(['325','326']),
        'certification' : True
    })

db.reservations.insert_many(fieldArray)
db.reservations.insert_many(tomorrowArray)
