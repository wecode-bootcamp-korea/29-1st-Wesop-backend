from django.urls import path
from users.views import CheckEmailView

urlpatterns = [
    path("emailvalid", CheckEmailView.as_view()),
]