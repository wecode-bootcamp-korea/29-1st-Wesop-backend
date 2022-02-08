from django.urls import path
from carts.views import AddCartView, UpdateCartView, DeleteCartView

urlpatterns = [
    path("add", AddCartView.as_view()),
    path("update",UpdateCartView.as_view()),
    path("delete", DeleteCartView.as_view())
]