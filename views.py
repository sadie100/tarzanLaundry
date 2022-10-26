
from flask import Flask, jsonify, render_template, request, make_response, flash, redirect, url_for
from datetime import datetime
from pymongo import MongoClient
# 준철 
import jwt

app = Flask(__name__)

# db 이름은 laundryDB로 통일
client = MongoClient('localhost',27017)
db = client.laundryDB

# 테스트용 어드민 아이디
adminID = 'kjc08'
adminPW = '0814'



## HTML을 주는 부분
@app.route('/')
def home():

   todayReservations = [
      { 'type' : 'laundry', 'room' : '325', 'day' : 10-29, 'time' : 7 },
      { 'type' : 'dry', 'room' : '326',  'time' : 10,  },
      { 'type' : 'laundry', 'room' : '325', 'time' : 11 },
      { 'type' : 'laundry', 'room' : '325','time' : 11 },
      { 'type' : 'dry', 'room': '325',  'time' : 11 },
      { 'type' : 'laundry', 'room' : '325',  'time' : 12 },
      { 'type' : 'laundry', 'room' : '325',  'time' : 14 },
      { 'type' : 'dry', 'room' : '325',  'time' : 18 },
      { 'type' : 'laundry', 'room' : '325',  'time' :20 ,'id': None},
      { 'type' : 'dry', 'room' : '325',  'time': 22 ,'id':'kjc0000'}
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


@app.route('/login',methods=['POST'])
def login():
   # 인풋 데이터 불러오기
   input_id = request.form.get('input_id')
   input_pw = request.form.get('input_password')
   print(input_id,input_pw)
   if db.users.find_one({'id':input_id}) or input_id == adminID:
      # 테스트에서 없는 데이터의 벨류값을 찾을 경우 에러가 발생해서 주석처리함.
      # 추후 회원 데이터가 생기면 업데이트 해야함
      # input_pw == db.users.find_one({'id':input_id})['password'] or
      if  input_pw == adminPW:

         # 로그인 성공 시 토큰 생성
         
         # jwt_token = jwt.encode(
         #    payload = {
         #       "key1" : "value1"
         #    }
         # )

         Token = 'abcd차차차'
         user_name = "준철"
         flash(f'{user_name}님 반갑습니다.{Token}은 토큰입니다!')
         return redirect(url_for('home'))
      else:
         flash('패스워드가 맞지 않습니다.')
         return redirect(url_for('home'))

   else :
      flash('가입되어 있지 않은 사용자입니다.')
      return redirect(url_for('home'))


if __name__ == '__main__': 
   # 시크릿 키 설정이 되어있지 않으면 submit 액션에서 보안오류 발생.
   # 또한 JWT 토큰 발행에 사용되는 시크릿 키 설정 필요.
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(debug=True)