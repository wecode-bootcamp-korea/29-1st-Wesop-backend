import json
import re
import bcrypt
import jwt

from django.views import View
from users.models import User

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM

class CheckEmailView(View) :
    def post(self, request) :
        try :
            recieve_email_data  = json.loads(request.body)
            email               = recieve_email_data['email']
            REG_EMAIL           = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
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
        try :
            input_data  = json.loads(request.body)
            email       = input_data['email']
            password    = input_data['password']

            REG_PASS    = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            REG_EMAIL   = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
            last_name   = input_data['last-name']
            first_name  = input_data['first-name']
            
            name        = last_name + '^' + first_name
            
            if not re.fullmatch(REG_EMAIL, email) :
                return JsonResponse({'message' : '유효하지 않은 이메일입니다'}) 
            if not re.fullmatch(REG_PASS,password) :
                return JsonResponse({'message' : '유효하지 않은 패스워드'},status = 401)
            if User.objects.filter(email__exact = email).exists() :
                return JsonResponse({"message" : "이미 가입된 이메일"}, status = 400)
            else :
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
        try :
            login_para  = json.loads(request.body)
            user        = User.objects.get(email__exact = login_para['email'])
            
            if bcrypt.checkpw(login_para['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = ALGORITHM)
                return JsonResponse({ 'message': 'SUCCESS','ACCESS_TOKEN' : access_token}, status = 200)
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