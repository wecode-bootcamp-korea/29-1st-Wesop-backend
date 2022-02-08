import json
import re

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from .models import MainCategory, SubCategory, Product

class MainCategoryListView(View):
    def get(self, request):
        main_categories      = MainCategory.objects.all()
        main_categories_list = [{"name": main_category.name} for main_category in main_categories]
        return JsonResponse({"main_categories": main_categories_list}, status=200)

class SubCategoryListView(View):
    def get(self, request):
        try:
            sub_categories      = SubCategory.objects.all()
            sub_categories_list = [{
                        "name"                     : sub_category.name,
                        "main_category_name"       : sub_category.main_category.name,
                        "main_category_id"         : sub_category.main_category.id,
                        "sub_category_id"          : sub_category.id,
                        "sub_category_description" : sub_category.description,
                    } for sub_category in sub_categories
                    ]
            return JsonResponse({"sub_categories": sub_categories_list}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class ProductListView(View):
    def get(self, request, *args, **kwargs):
        try:
            sub_category_id   = request.GET.get('categoryId', None)
            sub_category_name = request.GET.get('categoryName', None)
            skin_type         = request.GET.getlist('skinType', None)
            ingredient        = request.GET.getlist('ingredient', None)
            # sort              = request.GET.get('sort', None)
            # product_price     = request.GET.get('productPrice', None)

            q = Q()

            if sub_category_name:
                q.add(Q(sub_category__name=sub_category_name), q.OR)

            if sub_category_id:
                q.add(Q(sub_category=sub_category_id), q.AND)

            if skin_type:
                q.add(Q(product_skin_type__skin__name__in=skin_type), q.AND)

            if ingredient:
                q.add(Q(product_key_ingredient__ingredient__name__in=ingredient), q.AND)
        
            products = Product.objects.complex_filter(q).distinct()
            print(products)
            
            result = [{
                "sub_category_id"         : product.sub_category.id,
                "sub_category_name"       : product.sub_category.name,
                "sub_category_description": product.sub_category.description,
                "products"                : [{
                        "product_name"          : product.name,
                        "product_description"   : product.description,
                        "product_ingredient_etc": product.ingredients_etc,
                        "product_id"            : product.id,
                        "product_detail"        : [
                            {
                                "product_option_id" : product_option.id,
                                "size"              : product_option.size,
                                "price"             : product_option.price,
                            } for product_option in product.products_options.all()
                        ],
                        "key_ingredient": [
                        key_ingredient.ingredient.name for key_ingredient in product.product_key_ingredient.all()
                        ],
                        "skin_type" : [
                        skin_type.skin.name for skin_type in product.product_skin_type.all()
                        ],
                    }]
                } for product in products]
            
            return JsonResponse({"message": result}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Exception as e:
            return JsonResponse({"message": f"{e}"}, status=400)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product        = Product.objects.get(id=product_id)
            product_detail = {
                "name"                    : product.name,
                "description"             : product.description,
                "ingredients_etc"         : product.ingredients_etc,
                "sub_category_id"         : product.sub_category.id,
                "sub_category_name"       : product.sub_category.name,
                "sub_category_desciprtion": product.sub_category.description,
                "product_id"              : product.id,
                "product_detail"          : [
                    {
                        "product_option_id" : product_option.id,
                        "size"      : product_option.size,
                        "price"     : product_option.price,
                    } for product_option in product.products_options.all()
                ],
                "product_usage"           : [
                    {
                        "description": product_usage.description,
                        "dosage"     : product_usage.dosage,
                        "texture"    : product_usage.texture,
                        "aroma"      : product_usage.aroma,
                        "image_url"  : product_usage.image_url
                    }
                    for product_usage in product.products_usages.all()
                ],
                "key_ingredient"   : [
                    key_ingredient.ingredient.name
                    for key_ingredient in product.product_key_ingredient.all()
                ],
                "skin_type"        : [
                    skin_type.skin.name
                    for skin_type in product.product_skin_type.all()
                ],
            }
            return JsonResponse({"message": product_detail}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"message": "PROUDCT_DOES_NOT_EXIST"}, status=400)
