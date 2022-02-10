from django.urls import path
from carts.views import CartView

urlpatterns = [
    path("", CartView.as_view()),     
    path("/add",CartView.as_view()),
    path("/update/<int:option_id>",CartView.as_view()),
    path("/delete/<int:option_id>",CartView.as_view())
]