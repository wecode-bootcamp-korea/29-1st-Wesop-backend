from django.urls import URLPattern, path

from .views import MainCategoryListView, SubCategoryListView, ProductListView, ProductView
urlpatterns = [
    path('', MainCategoryListView.as_view()),
    path('categories', SubCategoryListView.as_view()),
    path('skin/products/<int:product_id>', ProductView.as_view()),
    path('skin/products', ProductListView.as_view()),
]
