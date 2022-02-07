import json

from django.http import JsonResponse
from django.views import View

from cart.models import Cart
from products.models import Product

class AddCartView(View) :
    def post (self, request) :
        try :
            print("request head")
            print("-----------------")
            print (request.headers)
            print("-----------------")
            request_data   = json(request.body)
            user_id     = request_data['user_id']
            product_id  = request_data['product_id']

            if user_id != '' and  product_id !='' :
                Cart.object.create(
                    users_id    = user_id,
                    product_id  = product_id
                )
                
                # 성공적으로 조회response 생성
                # 그냥... 
                price = int(Product.objects.filter(id= product_id)['price'])
                response_data = dict()
                response_data['url'] = request.headers.url
                response_data['result'] = 'SUCCESS',
                response_data['message']['product_id'] = product_id
                response_data['message']['product_price'] = price
                response_data['message']['product_count'] = 1


                
                return JsonResponse(response_data, status = 201)
            else :
                return JsonResponse({"message" : "valueError"}, status= 401) 
        except KeyError as KE_1 :
            return 1
        except KeyError as KE_2 :
            return 1
        except ValueError as VE_1 :
            return JsonResponse({}, status = 401)
        except Cart.DoesNotExist :
            return 1
        

class UpdateCartCountView (View) :
    def post(self, request) :
        return 1

class DeleteCartContView (View) :
    def post(self, request) :
        return 1