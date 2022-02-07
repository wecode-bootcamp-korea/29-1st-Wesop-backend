from django.urls import URLPattern, path

from .views import MainCategoryView, SubCategoryView, ProductView, SubCategoryProductView

urlpatterns = [
    path('', MainCategoryView.as_view()),
    path('categories', SubCategoryView.as_view()),
    path('skin/products/<int:product_id>', ProductView.as_view()),
    path('sub_categories/<int:sub_category_id>', ProductListView.as_view()),
]

