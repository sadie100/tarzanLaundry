
from flask import Flask, jsonify, render_template, request, make_response, flash, redirect, url_for
from datetime import datetime, date, timedelta
from pymongo import MongoClient
# 준철 
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,decode_token,
     create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

app.config['JWT_SESSION_COOKIE'] = False

app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# 토큰의 쿠키에 대하여 이름을 부여. 해당 이름으로 쿠키를 찾는다
app.config['JWT_ACCESS_COOKIE_NAME'] = 'myapp_jwt'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'myapp_jwt_refresh'

app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['JWT_COOKIE_SECURE'] = False

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


from pymongo import MongoClient
# db 이름은 laundryDB로 통일
client = MongoClient('localhost',27017)
db = client.laundryDB

# 테스트용 어드민 아이디
adminID = 'kjc08'
adminPW = '0814'

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
   },{ '_id':0, 'user':1, 'type':1, 'room':1, 'date':1}).sort([['time',1]]))

   for x in todayReservations:
      x['time'] = x['date'].hour
      del x['date']

   tomorrowReservations = list(db.reservations.find({
      'date' : {'$gte' : exactTomorrow, '$lt':exactDat}
   }, { '_id':0, 'user':1, 'type':1, 'room':1, 'date':1}).sort([['time',1]]))

   for x in tomorrowReservations:
      x['time'] = x['date'].hour
      del x['date']

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
   using = request.cookies.get('myapp_jwt')
   # 만약 로그인 했으면 해당 사용자의 id 값을 읽는다
   if using :
      decodeInfo = decode_token(request.cookies.get('myapp_jwt'))
      userId = decodeInfo['sub']
      return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, nowtime=nowtime, using=using, userId=userId)
   return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, nowtime=nowtime, using=using, userId=False)


# 토큰 식별 과정 (토큰이 있어야 정상작동)
# 웹에서 사용하지는 않음
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# 로그인 submit 버튼 눌렀을 때 작동
@app.route('/login',methods=['POST'])
def login():
   # input 데이터 불러오기
   input_id = request.form.get('input_id')
   input_pw = request.form.get('input_password')
   
   # 아이디가 존재하는지 확인
   if db.users.find_one({'id':input_id}) or input_id == adminID:
      # 테스트에서 없는 데이터의 벨류값을 찾을 경우 에러가 발생해서 주석처리함.
      # input_pw == db.users.find_one({'id':input_id})['password'] or
      # 추후 회원 데이터가 생기면 업데이트 해야함

      # 패스워드 일치하는지 확인
      if  input_pw == adminPW:

         # 토큰에 추가할 추가 정보는 additional_claims 에 입력
         additional_claims = {"로그인 여부": "ON"}
         # 로그인 성공 시 토큰 생성
         access_token = create_access_token(input_id, additional_claims=additional_claims)
         resp = make_response(redirect(url_for('home')))
         set_access_cookies(resp, access_token)
         flash(f'{input_id}님 반갑습니다.{access_token}은(는) 당신의 토큰입니다!')
         return resp
      else:
         flash('패스워드가 맞지 않습니다.')
         print('패스워드 잘못됨')
         return redirect(url_for('home'))

   else :
      flash('가입되어 있지 않은 사용자입니다.')
      return redirect(url_for('home'))

@app.route('/logout',methods=['GET'])
def logout():
   print("로그아웃을 눌렀다")

   response = make_response(redirect(url_for("home")))
   unset_jwt_cookies(response)
   flash('로그아웃했습니다.')

   return response


if __name__ == '__main__': 
   # 시크릿 키 설정이 되어있지 않으면 submit 액션에서 보안오류 발생.
   app.secret_key = "super-secret"
   # app.config['SESSION_TYPE'] = 'filesystem'
   app.run(debug=True)
