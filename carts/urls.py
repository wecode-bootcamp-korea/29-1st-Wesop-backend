from django.urls import path, include
from carts.views import AddCartView

urlpatterns = [
    path("addcart", AddCartView.as_view())
]