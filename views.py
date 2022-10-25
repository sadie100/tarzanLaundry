from flask import Flask, render_template, request
app = Flask(__name__)

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('table.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)