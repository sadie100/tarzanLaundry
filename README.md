# tarzanLaundry

templates : html 파일 담겨 있는 폴더

## 버전 관리 하는 법

git에 .venv 내 파일들을 직접 올리는 것은 충돌 및 에러의 위험이 크다

(출처 : https://somjang.tistory.com/entry/Git-gitignore-%EC%9D%84-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%ED%95%84%EC%9A%94%EC%97%86%EB%8A%94-%ED%8C%8C%EC%9D%BC-%EC%A0%9C%EC%99%B8%ED%95%98%EA%B3%A0-%EC%97%85%EB%A1%9C%EB%93%9C%ED%95%98%EA%B8%B0)

따라서 gitignore에 .venv 이하 파일을 추가하였음

### pip install한 목록을 git에 공유하는 법

https://itholic.github.io/python-requirements/ 참고

터미널에 다음 명령어를 입력한다.

pip freeze > requirements.txt

그러면 requirements.txt에 패키지 버전 목록이 나열되게 된다. 이 파일을 git으로 저장할 것임

### requirements.txt로 pip install을 하는 법

우선 가상환경을 따로 실행한다.

py -3 -m venv .venv
//생성
.venv/Scripts/activate
//활성화

터미널에 다음 명령어를 입력한다.

pip install -r requirements.txt

그러면 모든 패키지를 한 번에 설치해준다.

requirements.txt가 변경되면(누군가 커밋하면) 다른 받는 사람은 이 설치 프로세스를 실행해 준다.
