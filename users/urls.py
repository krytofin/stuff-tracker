from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.userLogin, name="login"),
    path("register/", views.userRegister, name="register"),
    path("logout/", views.LogoutPage, name="logout"),
]
