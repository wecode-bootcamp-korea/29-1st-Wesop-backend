import json
import re

from django.views import View
from django.http import JsonResponse

from .models import MainCategory, SubCategory, Product


class MainCategoryListView(View):
    def get(self, request):
        main_categories = MainCategory.objects.all()
        results         = [{"name" : main_category.name} for main_category in main_categories]
        return JsonResponse({"main_categories": main_categories_list}, status=200)

class SubCategoryListView(View):
    # 위코드를 참고해서 리펙토링 해주세요.
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

class ProductListView(View):
    def get(self, request):
        # 127.0.0.1:8000/products // 모든 스킬
        # 127.0.0.1:8000/products?sub_category_id=1 
        try:
            sub_category_id = request.GET.get('subCategoryId')
            products        = Product.objects.filter(sub_category_id=sub_category_id).select_related('sub_category')
 
            """ list-comp 으로 수정해주세요.
            results = []
            requested_sub_category_products = []

            for product in sub_category_products:
                requested_sub_category_products.append(
                    {
                        "name"             : product.name,
                        "description"      : product.description,
                        "ingredients_etc"  : product.ingredients_etc,
                        "sub_category_id"  : product.sub_category.id,
                        "sub_category_name": product.sub_category.name,
                        "products_options" : [
                            {
                                "size"      : product_option.size,
                                "price"     : product_option.price,
                                "product_id": product.id
                            } for product_option in product.products_options.all()
                        ] 
                    }
                )

            return JsonResponse({"message": requested_sub_category_products}, status=200)
            """

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

import logging

logger = logging.getLogger()

class ProductView(View):
#    def post(self, request):
#        data = json.load(request.body)
#
#        try:
#            name            = data["name"]
#            description     = data["description"]
#            ingredients_etc = data["ingredients_etc"]
#            sub_category_id = data["sub_category_id"]
#
#            MainCategory.objects.create(
#                name            = name,
#                description     = description,
#                ingredients_etc = ingredients_etc,
#                sub_category_id = sub_category_id
#            )
#            return JsonResponse({"message":"SUCCESS"}, status=201)
#        except KeyError as e:
#            logger.error(f"error_message : {e}")
#            return JsonResponse({"message":"KEY_ERROR"}, status=400)
#    
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id).select_related().prefetch_related()

            result = {
                "name"             : product.name,
                "desciprtion"      : product.description,
                "ingredients_etc"  : product.ingredients_etc,
                "sub_category_id"  : product.sub_category.id,
                "sub_category_name": product.sub_category.name,
                "product_detail"   : [
                    {
                        "size"      : product_option.size,
                        "price"     : product_option.price,
                        "product_id": product.id
                    } for product_option in product.products_options.all()
                ],
                "key_ingredient"   : [
                    {
                        "name": key_ingredient.ingredient.name
                    } for key_ingredient in product.product_key_ingredient.all()
                ],
                "skin_type"        : [
                    {
                        "name": skin_type.skin.name
                    } for skin_type in product.product_skin_type.all()
                ],
            }

            return JsonResponse({"message": requested_product_detail}, status=200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except Product.DoesNotExist:
            return ..
