import json
import re
import bcrypt
import jwt

from django.views import View
from users.models import User

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM

class CheckEmailView(View) :
    """
        목적:로그인, 혹은 회원가입을 위한 이메일 유효성검사와 
        해당이메일을 기준으로 신규인지 기존회원인지 확인해주는 기능
        recived_data :: email
        1. 이메일 유효성 충족 했고 기존 회원인 경우 :
        {
            "message" : "이미 존재하는 회원"
        }
        2. 이메일 유효성 충족했지만 회원이 아닌경우 :
        {
            "message" : "유효한 이메일, 가입가능"
        }
        3. 이메일 유효성을 충족하지 않은 경우 :
        {
            "message" : "INVALID_EMAIL-잘못된 형식" , status = 401
        }
        4. 이메일 파라미터는 있으나 이메일 값은 없는 경우 :
        {
            "message" , "이메일 값 없음(email 키는 존재)",  status = 400
        }
        5. 파라미터이름이 없거나 잘못 전달된 경우
        {
            "message" , "이메일 값 없음(email파라미터 조차도 없음))",  status = 400
        }
        6. 이메일 키가 잘못된 경우 
        {
            "message" : "email 키 없음", status = 400
        }
    """
    def post(self, request) :
        try :
            email_data  = json.loads(request.body)
            email = email_data['email']
            REG_EMAIL = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            print(request.body)
            if email == '' :
                return JsonResponse({"message" : "이메일을 입력하세요"}, status = 400)
                        
            if not re.fullmatch(REG_EMAIL, email) : 
                return JsonResponse({"message" : "잘못된 형식의 이메일 입니다"}, status = 401)

            if User.objects.filter(email = email).exists() : 
                return JsonResponse({"message" : "이미 존재하는 회원", "sign-in" : 1}, status = 200)
            return JsonResponse({"message" : "유효한 이메일, 가입가능 ", "sign-in" : 0}, status  = 200)
        except KeyError :
            return JsonResponse({"message" : "email 키 없음"}, status = 400)
        except IndexError :
            return JsonResponse({"message" : "잘못된형식의 이메일(골뱅이없는)"}, status = 401)
        except json.JSONDecodeError :
            return JsonResponse({"message" : "잘못된형식의 이메일(email파라미터 조차도 없음))"}, status = 401)

class SignUpView (View) :
    def post(self, request) :
        """
        회원가입을 위한 기능 
        해당이메일을 기준으로 신규인지 기존회원인지 확인해줌
        비밀번호 유효성 검사를 해주고 first-name과 last-name을 받아서 이름으로 저장

        recived_data :: email,password
        1. 이메일, 패스워드 모두 유효하고 기존 회원이 아니면서 이름도 잘 전달 된 경우
        {
            "message" : "SUCCESS", status = 201
        }
        2. 이메일이 유효하고 이미 기존에 가입된 회원인 경우
        {
            "message" : "이미 가입된 이메일"
        }
        3. 비번이 유효하지 않은 경우
        {
            'message' : '유효하지 않은 패스워드'},status = 401
        }
        4. 일부 파라미터가 넘겨지지 않은 경우
        {
            'message' : '~을 입력하세요'},status = 401
        }
        5.바디에 파라미터가 없는 경우
        {
            "message" : "body에 어떤 것도 없음", status = 400
        }
        """
        try :
            input_data = json.loads(request.body)
            print("----------------")
            print(input_data)
            print("----------------")
            email = input_data['email']
            password = input_data['password']

            REG_PASS = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            REG_EMAIL = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
            first_name = input_data['first-name']
            last_name = input_data['last-name']
            
            name = first_name + '^' + last_name
            
            #이미 가입된 이메일인가?
            if not re.fullmatch(REG_EMAIL, email) :
                return JsonResponse({'message' : '유효하지 않은 이메일입니다'}) 
            if not re.fullmatch(REG_PASS,password) :
                return JsonResponse({'message' : '유효하지 않은 패스워드'},status = 401)
            if User.objects.filter(email__exact = email).exists() :
                return JsonResponse({"message" : "이미 가입된 이메일"}, status = 400)
            else :
                ## password 암호화
                User.objects.create(
                    email = email,
                    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    name = name
                )
                return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError :
            if 'first-name' or 'last-name' is None :
                return JsonResponse({"message" : "이름을 입력하세요"}, status = 400) 
            if 'email' is None :
                return JsonResponse({"message" : "이메일을 입력하세요"}, status = 400)
            if 'password' is None :
                return JsonResponse({"message" : "비밀 번호를 입력하세요"}, status = 400)
            else :
                return JsonResponse({"message" : "없는 파라미터 있음 혹은 파라미터 오타있음"}, status = 400)
        except json.JSONDecodeError :
            return JsonResponse({"message" : "body에 어떤 것도 없음"}, status = 400)

class LoginView (View) :
    def post (self , request) : 
        """
        로그인 기능
        이메일을 검색하고 비밀번호 비교를 통해서 로그인을 진행
        django_session table을 통해 로그인 상태인 경우 로그인 중이라는 메시지를 출력
        
        """
        try :
            login_para = json.loads(request.body)
            user = User.objects.get(email__exact = login_para['email'])
            print("----------------")
            print(login_para)
            print("----------------")
            print(bcrypt.checkpw(login_para['password'].encode('utf-8'), user.password.encode('utf-8')))
            
            if bcrypt.checkpw(login_para['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHM)
                return JsonResponse({'ACCESS_TOKEN' : access_token }, status = 200)
            else :
                return JsonResponse({"message": "로그인 실패"}, status = 401)
        
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except ValueError :
            return JsonResponse({"message": "INVALID_USER"}, status = 401)
        except User.DoesNotExist :
            return JsonResponse({"message ": "가입되지 않은 이메일"}, status = 400)
        except json.JSONDecodeError:
            return JsonResponse({"message" : "no-body"}, status = 400)
        except TypeError :
            return JsonResponse({"message": "가입안된 이메일"}, status = 400)