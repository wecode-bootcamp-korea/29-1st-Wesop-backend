from os import access
import re
import json
from tokenize import Pointfloat
import jwt

from django.http import JsonResponse
from django.views import View
from django.db.models import F

from carts.models import Cart
from users.models import User
from products.models import Product, ProductOption

from django.conf import settings

def validate_cartdata(func) :
    def wrapper(self, request) :
        try :
            data        = json.loads(request.body)
            data        = data["message"]
            
            user_id             = data["user_id"]
            product_option_id   = data["product_options_id"]
            user            =  User.objects.get(id = user_id)
            product_option  = ProductOption.objects.get(id = product_option_id)
        
        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_BODY_REQEUST"}, status = 400)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        except User.DoesNotExist :
            return JsonResponse({"message" : "INVALID_USER"}, status = 404)
        except ProductOption.DoesNotExist :
            return JsonResponse({"message" : "INVLALID_PRODUCT"}, status = 404)
        return func(self, request)
    return wrapper

def validate_quantity(func) :
    REX_INTEGER = r'^[+]{0,1}\d+$'
    def wrapper(self , request,**kargs) :
        try :
            data        = json.loads(request.body)
            data        = data["message"]
            quantity    = str(data["product_count"])

            if not re.fullmatch(REX_INTEGER,quantity) :
                return JsonResponse({"message" : "INVALID_VALUE"}, status = 400)

            check_integer = int(quantity)
            if check_integer <= 0 or check_integer > 4294967295 : 
                return JsonResponse({"message" : "INVALID_QUANTITY_RANGE"}, status = 400)
        
        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_BODY_REQEUST"}, status = 400)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)      
        return func(self, request,**kargs)
    return wrapper

def login_user(func) :
    def wrapper (self, request,**kargs) :
        try :
            print(**kargs)
            token   = kargs['token']
            print(token)
            user    = jwt.decode(token,settings.SECRET_KEY, algorithm = settings.ALGORITHM)
            if not User.objects.filter(id = user['id']).exists() :
                return JsonResponse({"message" : "INVALID_USER"}, status = 401) 
            return func(self, request, **kargs)
        except User.DoesNotExist :
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 401)
    return wrapper

def validate_product(func) :
    def wrapper(self, request,*args, **kargs):
        print(kargs)
        print(args)
        try :
            product_id =  kargs['product_options_id']
            if not ProductOption.objects.filter(id = product_id).exists() :
                return JsonResponse({"message" : "INVALID_PRODUCT"}, status=404)
            return func(self, request,*args, **kargs)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status=400)
    return wrapper

class GetCartListView(View) :
    @login_user
    def get(self, request, user_id) :

        user    = user_id
        items   = Cart.objects.filter(user_id = user).all().select_related('product').all().select_related('product').all()
        
        result = dict()
        result['user_id'] = user
        result['products'] = list()

        product = [
            {
            "product_options_id" : item.product.id,
            "product_name"       : item.product.product.name,
            "product_size"       : item.product.size,
            "product_count"      : item.quantity,
            "product_price"      : int(item.product.price)
            }for item in items  
        ]
        result['products'] = product
        result['message'] = "SUCCESS"

        return JsonResponse(result, status = 200)

class AddCartView(View) :
    @validate_cartdata
    def post (self, request) :
        try :
            data            = json.loads(request.body)['message']
            
            obj, create     = Cart.objects.get_or_create(
                user_id     =  data['user_id'] , 
                product_id  = data['product_options_id']
                )
            
            result = dict()
            
            if not create:
                obj.quantity = F('quantity') + 1
                obj.save()
                result['result'] = "SUCCESS_UPDATE"
                return JsonResponse(result,status= 201)
            
            item = Cart.objects.filter(product_id = data['product_options_id']).select_related('product').select_related('product').get()
            
            product = {
                "product_options_id" : item.product.id,
                "product_name"       : item.product.product.name,
                "product_size"       : item.product.size,
                "product_count"      : item.quantity,
                "product_price"      : int(item.product.price)
            }
            
            result["product"] = product
            result["result"] = "SUCCESS"
            
            return JsonResponse(result,status= 201)
        
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status= 400)
        except AttributeError :
            return JsonResponse({"message" : "SERVER_ERROR"},status= 500)

class UpdateCartView (View) :
    @validate_quantity
    def patch(self, request, user_id, product_id) :
        try :
            user = user_id
            product = product_id
            data            = json.loads(request.body)['message']
            
            obj, created    = Cart.objects.update_or_create( 
                        user_id     = user, 
                        product_id  =product
            )

            result = dict()
            result["product_count"] = data["product_count"]
            
            if not created:
                obj.quantity        = data["product_count"]
                obj.save()
                
                result["result"]    = "SUCCEESS"
                return JsonResponse(result,status= 201)
            
            result["result"]        = "SUCCEESS"
            return JsonResponse(result,status= 201)
        
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status= 400)

class DeleteCartView (View) :
    @validate_cartdata
    def post(self, request) :
        try :
            data = json.loads(request.body)['message']
            success  = Cart.objects.filter(
                user_id=data['user_id'],
                product_id=data['product_options_id']
            ).delete()
            if success == 0 :
                return JsonResponse({"message" : "DELETE_FAIL"}, status= 400)
            return JsonResponse({"message" : "DELETE_SUCCESS"}, status= 400)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status= 400)