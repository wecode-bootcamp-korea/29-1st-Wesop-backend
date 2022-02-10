import json
import re
import bcrypt
import jwt

from django.views import View
from users.models import User

from django.http import JsonResponse

from django.conf import settings


REG_PASS  = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

def validate_email(func):
    def wrapper(self, request) :
        """
        이메일 유효성 검사를 하는 validator
        """
        REGEX_EMAIL = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        try :
            data = json.loads(request.body)
            if not re.fullmatch(REGEX_EMAIL, data["email"]) : 
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 401)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_BODY_REQUEST"}, status = 401)
        return func(self, request)

    return wrapper

def validate_passoword(func) :
    def wrapper(self, request) :
        """
        비밀번호 유효성을 검사하는 validator
        """
        REG_PASS  = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        try :
            data = json.loads(request.body)
            if not re.fullmatch(REG_PASS, data["password"]) :
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 404)
        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 404)
        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_BODY_REQUEST"}, status = 401)
        return func(self, request)
    return wrapper

class EmailValidView (View):
    @validate_email
    def post(self, request):
        data = json.loads(request.body)
        
        if not User.objects.filter(email = data['email']).exists() : 
            return JsonResponse({"message" : "JOIN_POSSIBLE", "sign_in" : 0 }, status  = 200)
        
        return JsonResponse({"message" : "ALREADY_JOIN_USER", "sign_in" : 1 }, status = 404)
        

class SignUpView (View) :
    @validate_email
    @validate_passoword
    def post(self, request) :
        try :
            data       = json.loads(request.body)
            email      = data['email']
            password   = data['password']
            last_name  = data['last-name']
            first_name = data['first-name']
            name       = last_name + '^' + first_name
            
            if User.objects.filter(email__exact = email).exists() :
                return JsonResponse({"message" : "ALREADY_JOIN_USER"}, status = 400)

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
    @validate_email
    @validate_passoword
    def post (self , request) : 
        try :
            data = json.loads(request.body)
            user = User.objects.get(email__exact = data['email'])
            
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
                return JsonResponse({ 'message': 'SUCCESS','ACCESS_TOKEN' : access_token}, status = 200)

            return JsonResponse({"message": "FAIL_LOGIN"}, status = 401)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

        except User.DoesNotExist :
            return JsonResponse({"message": "NO_USER"}, status = 404)
        except json.JSONDecodeError:
            return JsonResponse({"message" : "INVALID_REQUEST_BODY"}, status = 400)