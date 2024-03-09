"""Define template for URL addresses in accounts project"""

from django.urls import path, include

from . import views

app_name = "accounts"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    url("register/", views.register, name="register"),
]
