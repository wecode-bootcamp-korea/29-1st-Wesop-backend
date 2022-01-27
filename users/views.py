import json
import re
import bcrypt
import jwt

from simplejson import JSONDecodeError

from django.views import View
from users.models import User

from django.http import JsonResponse

from my_settings import SECRET_KEY

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

            if email == '' :
                return JsonResponse({"message" : "이메일 값 없음(email 키는 존재)"}, status = 400)
                        
            if not re.fullmatch(REG_EMAIL, email) : 
                return JsonResponse({"message" : "INVALID_EMAIL-잘못된 형식"}, status = 401)

            if User.objects.filter(email = email).exists() : 
                return JsonResponse({"message" : "이미 존재하는 회원"}, status = 200)
            return JsonResponse({"message" : "유효한 이메일, 가입가능 "}, status  = 200)
        except KeyError :
            return JsonResponse({"message" : "email 키 없음"}, status = 400)
        except IndexError :
            return JsonResponse({"message" : "잘못된형식의 이메일(골뱅이없는)"}, status = 401)
        except json.JSONDecodeError :
            return JsonResponse({"message" : "잘못된형식의 이메일(email파라미터 조차도 없음))"}, status = 401)