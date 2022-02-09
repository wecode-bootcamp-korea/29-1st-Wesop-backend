from django.urls import path
from users.views import SignUpView, LoginView, EmailValidView

urlpatterns = [
    path("emailvalid", EmailValidView.as_view()), ##users/emailvalid
    path("signup",     SignUpView.as_view()), ## users/signUp
    path("login",     LoginView.as_view()) ## users/login
]