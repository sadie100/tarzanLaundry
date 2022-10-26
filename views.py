from datetime import datetime
from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():



   todayReservations = [
      { 'type' : 'laundry', 'room' : '325', 'time' : 7 },
      { 'type' : 'dry', 'room' : '326',  'time' : 10,  },
      { 'type' : 'laundry', 'room' : '325', 'time' : 11 },
      { 'type' : 'laundry', 'room' : '325','time' : 11 },
      { 'type' : 'dry', 'room': '325',  'time' : 11 },
      { 'type' : 'laundry', 'room' : '325',  'time' : 12 },
      { 'type' : 'laundry', 'room' : '325',  'time' : 14 },
      { 'type' : 'dry', 'room' : '325',  'time' : 18 },
      { 'type' : 'laundry', 'room' : '325',  'time' :20 },
      { 'type' : 'dry', 'room' : '325',  'time': 22 }
   ]

   tomorrowReservations = [
      { 'type' : 'laundry', 'room' : '325', 'time' : 7 },
      { 'type' : 'dry', 'room' : '326',  'time' : 7,  },
      { 'type' : 'laundry', 'room' : '325', 'time' : 8 },
      { 'type' : 'laundry', 'room' : '326','time' : 15 },
      { 'type' : 'dry', 'room': '326',  'time' : 14 },
      { 'type' : 'laundry', 'room' : '325',  'time' : 16 },
      { 'type' : 'laundry', 'room' : '326',  'time' : 16 },
      { 'type' : 'dry', 'room' : '326',  'time' : 19 },
      { 'type' : 'laundry', 'room' : '325',  'time' :19 },
      { 'type' : 'dry', 'room' : '325',  'time': 21 }, 
   ]

   nowtime = datetime.now()


   return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, nowtime=nowtime)

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)