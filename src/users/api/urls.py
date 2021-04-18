from django.urls import path, include
from . import views


app_name = "api"

urlpatterns = [
    path("create", views.UserCreateAPIView.as_view()),
    path("login", views.UserLoginViewJWT.as_view())
]
