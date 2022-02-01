from django.urls import path
from users.views import CheckEmailView, SignUpView, LoginView

urlpatterns = [
    path("emailvalid", CheckEmailView.as_view()), ##users/emailvalid
    path("signUp",     SignUpView.as_view()), ## users/signUp
    path("login",     LoginView.as_view()) ## users/login
]