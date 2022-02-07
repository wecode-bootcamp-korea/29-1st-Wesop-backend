from django.urls import path
from users.views import SignUpView, LoginView, check_email

urlpatterns = [
    path("emailvalid", check_email), ##users/emailvalid
    path("signUp", SignUpView.as_view()), ## users/signUp
    path("login", LoginView.as_view()) ## users/login
]
