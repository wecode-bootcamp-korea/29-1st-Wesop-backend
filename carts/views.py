import json

from django.http import JsonResponse
from django.views import View
from django.db.models import F

from carts.models import Cart

from .utils  import validate_quantity, validate_product , confirm_login, validate_cart

class CartView(View):

    @confirm_login
    def get(self, request, *args, **kargs) :
        try :
            user = kargs['user_id']
            cart_items = Cart.objects.filter(user_id = user).select_related('product').select_related('product').all()
            result =  dict()
            
            products = [
                {
                    "option_id" : item.product_id,
                    "name"       : item.product.product.name,
                    "size"       : item.product.size,
                    "count"      : item.quantity,
                    "price"      : int(item.product.price),
                    'option'     : [ ## 프론트 요청 리팩토링시 삭제 예정
                       {'value' : 1},
                       {'value' : 2},
                       {'value' : 3},
                       {'value' : 4},
                       {'value' : 5}, 
                    ] 
                }for item in cart_items
            ]
            result['products'] = products

            result['result'] = "SUCCESS"
        except KeyError :
            return JsonResponse(result, status = 400)
        return JsonResponse(result, status = 200)
    
    @confirm_login
    @validate_product
    def post (self,request, *args, **kargs) :
        try :
            obj, create     = Cart.objects.get_or_create(
                user_id     = kargs['user_id'] , 
                product_id  = kargs['option_id']
            )

            result = dict()
            
            if not create:
                obj.quantity = F('quantity') + 1
                obj.save()
                result['result'] = "SUCCESS_UPDATE"
                return JsonResponse(result,status= 201)

            item = Cart.objects.filter(
                product_id = kargs['option_id'],user_id = kargs['user_id']
                ).select_related('product').select_related('product').get()
            product = {
                "option_id"  : item.product.id,
                "name"       : item.product.product.name,
                "size"       : item.product.size,
                "count"      : item.quantity,
                "price"      : int(item.product.price)
            }
            result["product"]   = product
            result["result"]    = "SUCCESS"
            
            return JsonResponse(result,status= 201)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status= 400)
        except AttributeError :
            return JsonResponse({"message" : "SERVER_ERROR"},status= 500)
    
    @confirm_login
    @validate_quantity
    @validate_cart
    def patch(self, request,*args, **kargs) :
        try :                   
            user_id = kargs['user_id']
            option_id = kargs['option_id']
            obj, created    = Cart.objects.update_or_create( 
                    user_id     = user_id,
                    product_id  = option_id 
            )
            result = dict()
            result["product_count"] = kargs["product_count"]
            
            if not created:
                obj.quantity        = kargs["product_count"]
                obj.save()
                result["result"]    = "SUCCEESS"
                return JsonResponse(result,status= 201)
            
            result["result"]        = "SUCCESS"
            return JsonResponse(result,status= 201)
        
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"},status= 400)

    @confirm_login
    @validate_cart
    def delete(self, request, *args,**kargs) :
        try :
            success  = Cart.objects.filter(
                user_id     = kargs['user_id'],
                product_id  = kargs['option_id']
            ).delete()
            
            result = dict()
            if success == 0 :
                result['result'] = "DELETE_FAIL"
                return JsonResponse(result, status= 400)
            result['result'] = "DELETE_SUCCESS"    
            return JsonResponse(result, status= 200)
        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status= 400)
        except NameError :
            return JsonResponse({"message" : "INVALID_PARA"},status = 400)