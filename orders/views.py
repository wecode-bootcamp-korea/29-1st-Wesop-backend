import json
import re

from django.views import View
from users.models import User
from products.models import Product, ProductOption

from django.http import JsonResponse

class loadCartView(View) :
    def post (self, request) :
        """
        회원 세션 확인하고(아직 안넣음)
        회원 아이디와 매치되는 카트 리스트를 반환한다.
        성공
        1.  카트가 비어있는 경우
        {
            "message" : "SUCCESS" , "cart" : 0 , status = 200
        }
        2. 카트가 비어있지 않은 경우
        {
            "message" : "SUCCESS" ,  
            "cart" : 
            [
                {
                   "product-id"    : 1
                    "product-name"  : 'p1'
                    "product-size"  : '100ml'
                    "count"         : 1
                    "price"         : 15000 #제품 1개의 가격, 프론트는 count * price 로 총 가격을 클라이언트 사이트에 게시한다.
                },
                {
                    "product-id"    : 2
                    "product-name"  : 'p2'
                    "product-size"  : '200ml'
                    "count"         : 2
                    "price"         : 12000
                }, 
                ...
            ]
            }
            실패 
            1. 세션 만료시
            {
                "message" : "FAIL_SESSION_EXPRIRED", status = 401
            }
            2. 비유효한 유저(유저id가 없는 유저를 참조한경우)
            {
                "message" : "INVALID_USER", status = 401 
            }
            3. 비유효한 상품(상품id가 없는 제품을 참조한 경우)
            {
                "message" : "INVALID_USER", status = 401
            }
            4. product_stock이 0개인 경우
            {
                "message" : "FAIL_SOLDOUT", status = 400
            }
            5. KEY_ERROR
            {
                "message" : "KEY_ERROR", status = 400
            }
        """
        try :
            para_data = json(request.body)
        except KeyError as ke :
            return JsonResponse()
        

class AddCartView(View) :
    def post (self, request) : 
        """
        회원 Cart 추가 기능 실행
        기본적으로 추가하면 1개가 더 추가됨
        request parameter
        body
        {
            token : token
            user_id : user_id
            product_id : product_id
        }
        성공시
        {
            'message' : 'SUCCESS_ADD_CART',
            status = 201
        }
        실패시
        1. product stock이 모자란 경우
        {
            'message' : 'FAIL_PRODUCT_SOLDOUT'
            status = 400 #버튼 비활성화 시길 것
        }
        2. KEY ERROR
        {
            'message' : 'KEY_ERROR',
            status = 400
        }
        3. 상품 아이디가 존재하지 않는 경우
        {
            'message' : 'INVALID_PRODUCT'
        }
        4. 사용자 아이디가 존재하지 않는 경우
        {
            'message' : 'INVALID_USER'
        }
        5. 세션이 만료된 경우
        {
            'message' : 'INVALID_SESSION'
        }
        6. 그 외 DB관련 에러시
        {
            'message' : 'DBERROR'
            status = 500
        }
        """
        
class UpdateCartCountView (View) :
    def post (self, request) :
        """
        카트 내 수량 변경 프론트에서 1~5사이의 값이 오기때문에 
        그것으로 수정된다. 혹여나 이상한 값이 온 경우 1로 고정해서 저장해 준다
        성공시 "
        {
            "message"   : "SUCCESS : UPDATE PRODUCT STOCK" ,
            status = 201
        }

        경고 
        1. 재고가 없는 제품인 경우 ->product 재고를 넘기지 않은 선에서 STOCK을 리턴함 , 
        {
            "message"   : "CAUSION : PRODUCT SOLDOUT",
            "stock"     : [최대로 추가 될 갯수] ,
            status = 201
        }

        실패시
        1. 장바구니에 담기지 않은 제품인 경우 데이터 베이스 오류인 경우:
        {
            "message" : "FAIL : PRODUCT NOT IN YOUR CART",
            status = 400
        }
        2. 유저가 없는 경우 (비유효한 유저인 경우)
        {
            "message" : "FAIL : INVALID USER",
            status = 400
        }
        """

class DeleteCartContView (View) :
    def post(self, request) :
        """
        회원 카트(장바구니) 제품 삭제하기
        user cart에 담긴 제품 정보를 삭제
        request 시
        {
            'user-id' : 'user_id',
            'product-id' : 'product_id' 
        }
        성공
        {
            "message" : "SUCCESS",
            status  = 200
        }
        """