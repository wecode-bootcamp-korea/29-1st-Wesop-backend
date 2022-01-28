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

class ProductView(View):
    def get(self, request, product_id):
        try:
            requested_product = Product.objects.get(id=product_id)

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
                    ]
                }
            ]
            return JsonResponse({"message": requested_product_detail}, status=200)
        except KeyError as e:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)
