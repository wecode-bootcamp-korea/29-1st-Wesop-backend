import re
import json
from urllib import request
import jwt

from django.http import JsonResponse

from carts.models import Cart, User
from my_settings import SECRET_KEY , ALGORITHM
from products.models import ProductOption

from django.conf import settings

def confirm_login(func) :
    def wrapper (self, request,*args,**kargs) :
        try :
            token   = request.headers.get("Authorization", None)
            if token :
                user_token       = jwt.decode(token,SECRET_KEY,algorithms= ALGORITHM)
                user             = User.objects.get(id = user_token['id'])
                request.user     = user
                kargs['user_id'] = user_token['id']
                return func(self, request,*args, **kargs)
            return JsonResponse({"message" : "NEED_LOGIN"}, status = 401)
        
        except User.DoesNotExist :
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 401)
        except jwt.exceptions.InvalidSignatureError :
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 401)
        except jwt.exceptions.DecodeError :
            return JsonResponse({"message" : "DECODE_ERROR"}, status= 500)
    return wrapper

def validate_product(func) :
    def wrapper(self, request,*args, **kargs):
        try :
            data        = json.loads(request.body)
            option_id   = data['option_id']

            if not ProductOption.objects.filter(id = option_id).exists() :
                return JsonResponse({"message" : "INVALID_PRODUCT"}, status=404)
            
            kargs['option_id'] = option_id
            return func(self, request,*args, **kargs)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status=400)
    return wrapper

def validate_quantity(func) :
    REX_INTEGER = r'^[+]{0,1}\d+$'

    def wrapper(self , request,**kargs) :
        try :
            data        = json.loads(request.body)
            quantity    = str(data["product_count"])

            if not re.fullmatch(REX_INTEGER,quantity) :
                return JsonResponse({"message" : "INVALID_VALUE"}, status = 400)

            check_integer = int(quantity)
            if check_integer <= 0 or check_integer > 4294967295 : 
                return JsonResponse({"message" : "INVALID_QUANTITY_RANGE"}, status = 400)
            
            kargs['product_count'] =  quantity
            return func(self, request,**kargs)
        
        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_BODY_REQEUST"}, status = 400)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)      
        
    return wrapper

def validate_cart(func) :
    def wrapper (self, request, *args, **kargs) :
        try :
            if not Cart.objects.filter(
                user_id=kargs['user_id'],
                product_id = kargs['option_id']
                ).exists() :
                return JsonResponse({"message" : "NOT_IN_CART"},status = 404)
            return func(self, request, *args, **kargs)
        
        except NameError :
            return JsonResponse({"message" : "INVALID_PARA"},status = 400)
    return wrapper