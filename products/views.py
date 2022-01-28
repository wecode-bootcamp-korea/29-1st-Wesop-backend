from itertools import product
import json
from pydoc import describe
import re

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import MainCategory, SubCategory, Product, ProductOption, KeyIngredient, ProductIngredient, Skintype, ProductSkintype

class MainCategoryView(View):
    def post(self, request):
        data = json.load(request.body)

        try:
            name = data["name"]
            MainCategory.objects.create(
                name = name
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)
        except KeyError as e:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)  

    def get(self, request):
        main_categories      = MainCategory.objects.all()
        main_categories_list = []

        try:
            for main_category in main_categories:
                main_categories_list.append(
                    {
                        "name": main_category.name
                    }
                ) 
            return JsonResponse({"main_categories": main_categories_list}, status=200)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)

class SubCategoryView(View):
    def get(self, request):
        try:
            sub_categories      = SubCategory.objects.all()
            sub_categories_list = []

            for sub_category in sub_categories:
                sub_categories_list.append(
                    {
                        "name"              : sub_category.name,
                        "main_category_name": sub_category.main_category.name,
                        "main_category_id"  : sub_category.main_category.id
                    }
                ) 
            return JsonResponse({"sub_categories": sub_categories_list}, status=200)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)

class SubCategoryProductView(View):
    def get(self, request, sub_category_id):
        try:
            sub_category_products = Product.objects.filter(sub_category_id=sub_category_id)
            # 서브 카고리에 해당하는 제품을 모두 출력
            print(list(sub_category_products))
            requested_sub_category_products = []

            for product in sub_category_products:
                requested_sub_category_products.append(
                    {
                    "name"             : product.name,
                    "description"      : product.description,
                    "ingredients_etc"  : product.ingredients_etc,
                    "sub_category_id"  : product.sub_category.id,
                    "sub_category_name": product.sub_category.name,
                    "product_detail"   : [
                        {
                            "size"      : product_option.size,
                            "price"     : product_option.price,
                            "product_id": product.id
                        } for product_option in product.products_options.all()
                    ] 
                }
                )
            
            # a = requested_sub_category_products[1]
            # print(a["description"])

            return JsonResponse({"message": requested_sub_category_products}, status=200)
        except KeyError as e:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)


class ProductView(View):
    def post(self, request):
        data = json.load(request.body)

        try:
            name            = data["name"]
            description     = data["description"]
            ingredients_etc = data["ingredients_etc"]
            sub_category_id = data["sub_category_id"]

            MainCategory.objects.create(
                name            = name,
                description     = description,
                ingredients_etc = ingredients_etc,
                sub_category_id = sub_category_id
            )
            
            return JsonResponse({"message":"SUCCESS"}, status=201)
        except KeyError as e:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)  
    
    def get(self, request, product_id):
        try:
            requested_product    = Product.objects.get(id=product_id)
            products_ingredients = ProductIngredient.objects.filter(product_id=product_id)
            print(products_ingredients)
            
            products_ingredients_list = []

            # for product_ingredient in products_ingredients:
            #     products_ingredients_list.append(
            #         {

            #         }
            #     )

            print(len(list(products_ingredients)))
            # # p_list = []
            # # for p in pi:
            # #     print(p.ingredients_id)

            # pi_list = list(pi) 
            # result = []

            # for product_ingredient in pi_list:
            #     result.append(pi_list.ingredient_id)
            
            # print(result)
            # 제품 아이디가 == product_id일 때, 이에 맞는 KeyIngredient를 출력!
            
            # requested_product_key_ingredients = ProductIngredient.objects.all()
            # # for i in requested_product_key_ingredients:
            # #     print(i.__dict__)

            # ki = KeyIngredient.ingredients_set.all()
            # print(ki)

            # 여기서 해야 할 일은, 이 중간 테이블에서 FK가 물려있는 KeyIngredient로 가서
            # product_id = product_id에 해당하는 ingredients를 모아서
            # 제품 정보에 추가하여 보내주는 거지! 


            # requested_product_key_ingredients_detail = ProductIngredient.key_ingredients.all()
            # for j in requested_product_key_ingredients_detail:
            #     print(j.name)


            # for k in key_ingredients:
            #     print(k.name)

            # print(requested_product_key_ingredients)

            # 다른 방법으로 product_details 넣는 방법
            # requested_product_options = requested_product.products_options.all()            
            # for product_option in requested_product.products_options.all():
            #     print(product_option.size)

            requested_product_detail = [
                {
                    "name"             : requested_product.name,
                    "desciprtion"      : requested_product.description,
                    "ingredients_etc"  : requested_product.ingredients_etc,
                    "sub_category_id"  : requested_product.sub_category.id,
                    "sub_category_name": requested_product.sub_category.name,
                    "product_detail"   : [
                        {
                            "size"      : product_option.size,
                            "price"     : product_option.price,
                            "product_id": requested_product.id
                        } for product_option in requested_product.products_options.all()
                    ]                         #요청한 제품.related_name.all()
                    # "key_ingredient": [
                    #     {
                    #         "name": product_key_ingredient.name,
                    #     } for product_key_ingredient in requested_product.key_ingredients.all()
                    # ]
                }
            ]
            return JsonResponse({"message": requested_product_detail}, status=200)
        except KeyError as e:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)
