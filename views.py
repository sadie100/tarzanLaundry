from flask import Flask, render_template, request
from collections import deque
app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():
   todayReservations = deque([ { 'type' : 'laundry', 'room' : '325', 'username' :
'김철수', 'time' : 7, 'day' : 'today' }, { 'type' : 'dry', 'room' : '326', 'username'
: '홍길동', 'time' : 10, 'day' : 'today' }, { 'type' : 'laundry', 'room' : '325',
'username' : '홍길동', 'time' : 11, 'day' : 'today' }, { 'type' : 'laundry', 'room' :
'325', 'username' : '김철수', 'time' : 11, 'day' : 'today' }, { 'type' : 'dry', 'room'
: '325', 'username' : '김철수', 'time' : 11, 'day' : 'today' }, { 'type' :
'laundry', 'room' : '325', 'username' : '김철수', 'time' : 12, 'day' : 'today' }, {
'type' : 'laundry', 'room' : '325', 'username' : '김철수', 'time' : 14, 'day' :
'today' }, { 'type' : 'dry', 'room' : '325', 'username' : '김철수', 'time' : 18, 'day'
: 'today' }, { 'type' : 'laundry', 'room' : '325', 'username' : '김철수', 'time' :
20, 'day' : 'today' }, { 'type' : 'dry', 'room' : '325', 'username' : '김철수', 'time'
: 22, 'day' : 'today' }, ])

   return render_template('table.html', todayReservations=todayReservations)

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)