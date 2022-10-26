from flask import Flask, make_response, render_template, request
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
    { 'type' : 'dry', 'room' : '325',  'time': 21 }, ]

   now = 13

   return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, now=now)

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