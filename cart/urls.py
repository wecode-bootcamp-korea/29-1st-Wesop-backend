from django.urls import path, include
from cart.views import AddCartView

urlpatterns = [
    path("addcart", AddCartView.as_view())
]