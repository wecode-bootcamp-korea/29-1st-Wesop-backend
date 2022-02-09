from django.urls import path
from carts.views import AddCartView, UpdateCartView, DeleteCartView,GetCartListView

urlpatterns = [
    path("<int:user_id>", GetCartListView.as_view()),
    path("add", AddCartView.as_view()),
    path("update/<int:user_id>/<int:product_id>",UpdateCartView.as_view()),
    path("delete", DeleteCartView.as_view())
]