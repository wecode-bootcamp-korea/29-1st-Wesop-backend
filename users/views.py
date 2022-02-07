import json
import re
import bcrypt
import jwt

from django.views import View
from users.models import User

from django.http import JsonResponse
from django.conf import settings

def validate_email(user):
    REGEX_EMAIL = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.fullmatch(REG_EMAIL, data["email"]) : 
        raise Validator(error)

REG_PASS  = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

def check_email(request):
    try :
        data = json.loads(request.body)
        
        if not re.fullmatch(REG_EMAIL, data["email"]) : 
            return JsonResponse({"message" : "잘못된 형식의 이메일 입니다"}, status = 401)

        if User.objects.filter(email = data["email"]).exists() : 
            return JsonResponse({"message" : "이미 존재하는 회원", "sign-in" : 1}, status = 404)

        return JsonResponse({"message" : "유효한 이메일, 가입가능 ", "sign-in" : 0}, status  = 200)
    
    except KeyError :
        return JsonResponse({"message" : "email 키 없음"}, status = 400)

    except json.JSONDecodeError :
        return JsonResponse({"message" : "잘못된형식의 이메일(email파라미터 조차도 없음))"}, status = 401)


class SignUpView (View) :
    @input_validator
    def post(self, request) :
        try :
            data       = json.loads(request.body)
            email      = data['email']
            password   = data['password']
            last_name  = data['last-name']
            first_name = data['first-name']
            name       = last_name + '^' + first_name
            
            if not re.fullmatch(REG_EMAIL, email) :
                return JsonResponse({'message' : 'INVALID_EMIAL'}) 

            if not re.fullmatch(REG_PASS,password) :
                return JsonResponse({'message' : '유효하지 않은 패스워드'},status = 401)

            if User.objects.filter(email__exact = email).exists() :
                return JsonResponse({"message" : "이미 가입된 이메일"}, status = 400)

            User.objects.create(
                email = email,
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name = name
            )

            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_REQUEST_BODY"}, status = 400)

class LoginView (View) :
    @input_validator
    def post (self , request) : 
        try :
            data = json.loads(request.body)
            user = User.objects.get(email__exact = data['email'])
            
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.algorithm = ALGORITHM)
                return JsonResponse({ 'message': 'SUCCESS','ACCESS_TOKEN' : access_token}, status = 200)

            return JsonResponse({"message": "로그인 실패"}, status = 401)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

        except User.DoesNotExist :
            return JsonResponse({"message ": "가입되지 않은 이메일"}, status = 400)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "no-body"}, status = 400)
