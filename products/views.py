import json
import re

from django.views import View
from django.http import JsonResponse

from .models import MainCategory, SubCategory, Product
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 798c0e181ead8e286d04d738225b1d09b9491ea1

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
>>>>>>> e4d43012ba5cfe4b8fb8d5787b210d8d221fa386

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
    def get(self, request):
        try:
<<<<<<< HEAD
            if request.GET.get('categoryId'):
                sub_category_id = request.GET.get('categoryId')

                if int(sub_category_id) <= len(SubCategory.objects.all()):
                    products = Product.objects.filter(sub_category_id=sub_category_id)
                else:
                    raise Exception('CATEGORY_DOES_NOT_EXIST')
=======
            sub_category_products = Product.objects.filter(sub_category_id=sub_category_id)
            print(list(sub_category_products))
            requested_sub_category_products = []
>>>>>>> e4d43012ba5cfe4b8fb8d5787b210d8d221fa386

                result = [
                    {
<<<<<<< HEAD
<<<<<<< HEAD
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
                                        "size"      : product_option.size,
                                        "price"     : product_option.price,
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

            sub_categories = SubCategory.objects.all()
            result = []
            products   = [{
                    "sub_category_id"         : sub_category.id,
                    "sub_category_name"       : sub_category.name,
                    "sub_category_description": sub_category.description,
                    "products"                : [
                        {
                            "product_name"          : product.name,
                            "product_description"   : product.description,
                            "product_ingredient_etc": product.ingredients_etc,
                            "product_id"            : product.id,
                            "product_detail"        : [
                                {
                                    "size" : product_option.size,
                                    "price": product_option.price,
                                } for product_option in product.products_options.all()
                            ],
                    "key_ingredient"         : [
                        key_ingredient.ingredient.name for key_ingredient in product.product_key_ingredient.all()
                    ],
                    "skin_type"              : [
                        skin_type.skin.name for skin_type in product.product_skin_type.all()
                    ],
                        } for product in Product.objects.filter(sub_category_id=sub_category.id)
                    ],
            } for sub_category in sub_categories]
            result = products
            
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
=======
=======
>>>>>>> 798c0e181ead8e286d04d738225b1d09b9491ea1
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
                    ],
                    "key_ingredient"   : [
                        {
                            "name": key_ingredient.ingredient.name
                        } for key_ingredient in requested_product.product_key_ingredient.all()
                    ],
                    "skin_type"        : [
                        {
                            "name": skin_type.skin.name
                        } for skin_type in requested_product.product_skin_type.all()
                    ],
                }
            ]
            return JsonResponse({"message": requested_product_detail}, status=200)
        except KeyError as e:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"FAILED"}, status=400)
>>>>>>> e4d43012ba5cfe4b8fb8d5787b210d8d221fa386
