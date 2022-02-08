from pickletools import long1
import re
import json

from django.http import JsonResponse
from django.views import View
from django.db.models import F

from carts.models import Cart
from users.models import User
from products.models import Product, ProductOption

def validate_cartdata(func) :
    def wrapper(self, request) :
        try :
            data        = json.loads(request.body)
            data        = data["message"]
            
            user_id             = data["user_id"]
            product_option_id   = data["product_options_id"]
            user    =  User.objects.get(id = user_id)
            product_option = ProductOption.objects.get(id = product_option_id)
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
    def wrapper(self , request) :
        try :
            data        = json.loads(request.body)
            data        = data["message"]
            quantity    = str(data["product_count"])

            if not re.fullmatch(REX_INTEGER,quantity) :
                return JsonResponse({"message" : "VALUE_EROOR"}, status = 400)

            check_integer = int(quantity)
            if check_integer <= 0 or check_integer > 4294967295 : 
                return JsonResponse({"message" : "INVALID_QUANTITY_RANGE"}, status = 400)
        
        except json.JSONDecodeError :
            return JsonResponse({"message" : "INVALID_BODY_REQEUST"}, status = 400)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)      
        return func(self, request)
    return wrapper

class AddCartView(View) :
    @validate_cartdata
    def post (self, request) :
        try :
            data            = json.loads(request.body)['message']
            obj, create     = Cart.objects.get_or_create(
                user_id  =  data['user_id'] , 
                product_id = data['product_options_id']
                )
            
            ##여기에 json response 작성하기 
            result = dict()
            result["result"] = "SUCCESS"
            if not create:
                obj.quantity = F('quantity') + 1
                obj.save()
                return JsonResponse({"message" : "SECCESS_UPDATE_CART"},status= 201)
            
            return JsonResponse({"message" : "SUCCESS_ADD_CART"},status= 201)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status= 400)

class UpdateCartView (View) :
    @validate_cartdata
    @validate_quantity
    def post(self, request) :
        try :
            data            = json.loads(request.body)['message']
            
            obj, created    = Cart.objects.update_or_create( 
                            user_id=data['user_id'], 
                            product_id=data['product_options_id']
                            )
            result = dict()
            result["result"] = "SUCCEESS"
            
            if not created:
                obj.quantity = data["product_count"]
                obj.save()
                return JsonResponse({"message" : "SECCESS_UPDATE_CART"},status= 201)

            return JsonResponse({"message" : "SUCCESS_ADD_CART"},status= 201)
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