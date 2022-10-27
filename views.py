

from flask import Flask, jsonify, render_template, request, make_response, flash, redirect, url_for, abort
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

# jinja2에서 break문 사용하기 위한 extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

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
# client = MongoClient('mongodb://tarzan:jane@0.0.0.0',27017)   #서버 업로드
client = MongoClient('localhost',27017)                        #로컬 테스트
db = client.laundryDB


# 테스트용 어드민 아이디
adminID = 'kjc08'
adminPW = '0814'

# 토큰 만료 시
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
   print("토큰 만료")

   response = make_response(redirect(url_for("home")))
   unset_jwt_cookies(response)
   flash('로그인 정보가 만료됐습니다. 다시 로그인 해주세요.')

   return response

def get_table():
   today = date.today()
   exactToday = datetime(today.year,today.month,today.day)
   exactTomorrow = (datetime(today.year,today.month,today.day) + timedelta(days=1))
   exactDat =  (datetime(today.year,today.month,today.day) + timedelta(days=2))

   todayReservations = list(db.reservations.find({
      'date' : {'$gte' : exactToday, '$lt':exactTomorrow}
   },{ '_id':0, 'user':1, 'type':1, 'room':1, 'date':1}).sort([['date',1]]))

   for x in todayReservations:
      x['time'] = x['date'].hour
      del x['date']

   tomorrowReservations = list(db.reservations.find({
      'date' : {'$gte' : exactTomorrow, '$lt':exactDat}
   }, { '_id':0, 'user':1, 'type':1, 'room':1, 'date':1}).sort([['date',1]]))

   for x in tomorrowReservations:
      x['time'] = x['date'].hour
      del x['date']

   return todayReservations,tomorrowReservations

## HTML을 주는 부분
@app.route('/')
def home():
   todayReservations, tomorrowReservations = get_table()

   nowtime = datetime.now()
   using = request.cookies.get('myapp_jwt')
   # 만약 로그인 했으면 해당 사용자의 id 값을 읽는다
   
   if using :
      decodeInfo = decode_token(request.cookies.get('myapp_jwt'))
      userName = decodeInfo['이름']
      userId = decodeInfo['sub']

      today = date.today()
      myLaundry = db.reservations.find_one({'date' : {'$gte' : datetime(today.year,today.month,today.day,int(nowtime.hour))},'user': userId, 'type': 'laundry'})

      myDry = db.reservations.find_one({'date' : {'$gte' : datetime(today.year,today.month,today.day,int(nowtime.hour))},'user': userId, 'type': 'dry'})

      return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, nowtime=nowtime, using=using, userId=userId, userName=userName, myLaundry=myLaundry, myDry=myDry)
   return render_template('table.html', todayReservations=todayReservations,tomorrowReservations=tomorrowReservations, nowtime=nowtime, using=using, userId=False, userName=False,  myLaundry=False, myDry=False)


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
   if db.users.find_one({'user_id':input_id}):
      # 테스트에서 없는 데이터의 벨류값을 찾을 경우 에러가 발생해서 주석처리함.
      
      # 추후 회원 데이터가 생기면 업데이트 해야함

      # 패스워드 일치하는지 확인
      if  input_pw == db.users.find_one({'user_id':input_id})['user_pw']:

         # 토큰에 추가할 추가 정보는 additional_claims 에 입력
         my_name = db.users.find_one({'user_id':input_id})['user_name']
         additional_claims = {"이름":db.users.find_one({'user_id':input_id})['user_name'],"전화번호": db.users.find_one({'user_id':input_id})['user_phone']}
         # 로그인 성공 시 토큰 생성
         access_token = create_access_token(input_id, additional_claims=additional_claims)
         resp = make_response(redirect(url_for('home')))
         set_access_cookies(resp, access_token)
         flash(f'{my_name}님 반갑습니다.')
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


@app.route('/reserve', methods=['POST'])
def reserve():
   time = request.get_json()['time']
   day = request.get_json()['day']
   type = request.get_json()['type']
   room = request.get_json()['room']

   # 토큰 값 가져옴
   userId=False
   using = request.cookies.get('myapp_jwt')

   nowtime = datetime.now()
   today = date.today()
   tomorrow = (datetime(today.year,today.month,today.day) + timedelta(days=1))
   dateVal = date.today()
   # 만약 로그인 했으면 해당 사용자의 id 값을 읽는다
   if using :
      decodeInfo = decode_token(request.cookies.get('myapp_jwt'))
      userId = decodeInfo['sub']

      if db.reservations.find_one({'date' : {'$gte' : datetime(today.year,today.month,today.day,int(nowtime.hour))},'user': userId, 'type': type}):
         flash('더이상 예약하실 수 없습니다.')
         print('중복 예약')
         return jsonify({'state':'already'})
   else :
      # 에러 뱉기
      return abort(401)

   today = date.today()
   tomorrow = (datetime(today.year,today.month,today.day) + timedelta(days=1))
   dateVal = date.today()

   if day=='today':
      dateVal = datetime(today.year,today.month,today.day,int(time))
   elif day=='tomorrow':
      dateVal = datetime(tomorrow.year,tomorrow.month,tomorrow.day,int(time))

   db.reservations.insert_one({
      'date' : dateVal,
      'type' : type,
      'room' : room,
      'user' : userId,
      'certification' : False
   })

   return redirect(url_for('home'))

@app.route('/cancel', methods=['POST'])
def cancel():
   time = request.get_json()['time']
   day = request.get_json()['day']
   type = request.get_json()['type']
   room = request.get_json()['room']

   # 토큰 값 가져옴
   userId=False
   using = request.cookies.get('myapp_jwt')
   # 만약 로그인 했으면 해당 사용자의 id 값을 읽는다
   if using :
      decodeInfo = decode_token(request.cookies.get('myapp_jwt'))
      userId = decodeInfo['sub']
   else :
      # 에러 뱉기
      abort(401)

   today = date.today()
   tomorrow = (datetime(today.year,today.month,today.day) + timedelta(days=1))
   dateVal = date.today()

   if day=='today':
      dateVal = datetime(today.year,today.month,today.day,int(time))
   elif day=='tomorrow':
      dateVal = datetime(tomorrow.year,tomorrow.month,tomorrow.day,int(time))

   target = db.reservations.find_one({"date" : dateVal, "user" : userId, "type" : type, "room":room})
   if(target is None):
      abort(404)
   
   db.reservations.delete_one({
   "date" : dateVal, "user" : userId, "type" : type, "room":room
   })

   return redirect(url_for('home'))



@app.route('/signup')
def signup():
   return render_template('sign_up.html')

@app.route('/jungler_test')
def junglertest():
   return render_template('jungler_test.html')
   


@app.route('/signup/register',methods=['POST'])
def register():
   # 데이터 보내기
   if request.method == "POST":

      signup_id = request.get_json()   ['user_id'   ]
      signup_pw1 = request.get_json()  ['user_pw1'  ]
      signup_pw2 = request.get_json()  ['user_pw2'  ]
      signup_name = request.get_json() ['user_name' ]
      signup_room = request.get_json() ['user_room' ]
      signup_phone = request.get_json()['user_phone']


      if len(signup_id) < 4 :
         flash('아이디는 5자 이상입니다.')
         return redirect(url_for('register'))
      elif len(signup_name) < 2 :
         flash('이름은 2자 이상입니다..')
         return redirect(url_for('register'))
      elif signup_pw1 != signup_pw2 :
         flash('비밀번호가 서로 다릅니다.')
         return redirect(url_for('register'))
      elif len(signup_pw1) < 5 :
         flash('비밀번호가 너무 짧습니다.')
         return redirect(url_for('register'))

      else:
         if db.users.find_one({'user_id':signup_id}) == None:
            # 아이디 중복값

            if db.users.find_one({'user_phone':signup_phone}) == None:
               #전화번호 중복값 - 회원가입
               user_info = {'user_id':signup_id,'user_pw':signup_pw1,'user_name':signup_name,'user_room':signup_room,'user_phone':signup_phone}
               db.users.insert_one(user_info)
               flash(f'{signup_name}님 반갑습니다.{signup_pw1},{signup_name},{signup_room},{signup_phone} 입력정보')
               return redirect(url_for('home'))
               
            else: #전화번호 중복
               flash('중복된 전화번호 입니다.')
               return redirect(url_for('register'))

         else :
            flash('중복된 아이디 입니다.')
            return redirect(url_for('register'))



if __name__ == '__main__': 
   # 시크릿 키 설정이 되어있지 않으면 submit 액션에서 보안오류 발생.
   app.secret_key = "super-secret"
   # app.config['SESSION_TYPE'] = 'filesystem'
   # app.run('0.0.0.0', port=5000,debug=True)      #서버 업로드
   app.run(debug=True)                             #로컬 테스트
