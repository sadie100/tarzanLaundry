
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, make_response
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.laundryDB

def get_table():
   today = date.today()
   exactToday = datetime(today.year,today.month,today.day)
   exactTomorrow = (datetime(today.year,today.month,today.day) + timedelta(days=1))
   exactDat =  (datetime(today.year,today.month,today.day) + timedelta(days=2))

   # data = db.reservations.aggregate([
   #    {
   #       '$match':{
   #          'date':{
   #             '$gte' : exactToday,
   #             '$lt' : exactTomorrow
   #          }
   #       },
   #    },
   #    {
   #       '$project':{
   #          'user':1,
   #          'type':1,
   #          'room':1,
   #          'certification':1,
   #          'date':1,
   #          'time':{
   #             '$dateToString' : {
   #                'format' : '%H',
   #                'date' : '$date'
   #             }
   #          }
   #       }
   #    },
   #    {
   #       '$sort' : {
   #          'time' : 1
   #       }
   #    }
   # ])
   todayReservations = list(db.reservations.find({
      'date' : {'$gte' : exactToday, '$lt':exactTomorrow}
   }).sort([['time',1]]))


   for x in todayReservations:
      x['time'] = int(x['date'].hour)

   tomorrowReservations = list(db.reservations.find({
      'date' : {'$gte' : exactTomorrow, '$lt':exactDat}
   }).sort([['time',1]]))

   for x in tomorrowReservations:
      x['time'] = x['date'].hour

   return todayReservations,tomorrowReservations

## HTML을 주는 부분
@app.route('/')
def home():
   todayReservations, tomorrowReservations = get_table()
   # todayReservations = [
   #    { 'type' : 'laundry', 'room' : '325', 'day' : 10-29, 'time' : 7 },
   #    { 'type' : 'dry', 'room' : '326',  'time' : 10,  },
   #    { 'type' : 'laundry', 'room' : '325', 'time' : 11 },
   #    { 'type' : 'laundry', 'room' : '325','time' : 11 },
   #    { 'type' : 'dry', 'room': '325',  'time' : 11 },
   #    { 'type' : 'laundry', 'room' : '325',  'time' : 12 },
   #    { 'type' : 'laundry', 'room' : '325',  'time' : 14 },
   #    { 'type' : 'dry', 'room' : '325',  'time' : 18 },
   #    { 'type' : 'laundry', 'room' : '325',  'time' :20 ,'id': None},
   #    { 'type' : 'dry', 'room' : '325',  'time': 22 ,'id':'kjc0000'}
   # ]

   # tomorrowReservations = [
   #    { 'type' : 'laundry', 'room' : '325', 'time' : 7 },
   #    { 'type' : 'dry', 'room' : '326',  'time' : 7,  },
   #    { 'type' : 'laundry', 'room' : '325', 'time' : 8 },
   #    { 'type' : 'laundry', 'room' : '326','time' : 15 },
   #    { 'type' : 'dry', 'room': '326',  'time' : 14 },
   #    { 'type' : 'laundry', 'room' : '325',  'time' : 16 },
   #    { 'type' : 'laundry', 'room' : '326',  'time' : 16 },
   #    { 'type' : 'dry', 'room' : '326',  'time' : 19 },
   #    { 'type' : 'laundry', 'room' : '325',  'time' :19 },
   #    { 'type' : 'dry', 'room' : '325',  'time': 21 }, 
   # ]

   nowtime = datetime.now()


   return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, nowtime=nowtime)

@app.route('/memo')
def memo():
   info = "1212##12#"
   resp = make_response()
   resp.set_cookie('myinfo',info)
   return resp

@app.route('/get_cookie')
def get_cookie():
   print(request.cookies.get('myinfo'))
   return request.cookies.get('myinfo')
   




if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)