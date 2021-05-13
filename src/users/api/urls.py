from django.urls import path, include

from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register(r'', views.UserViewset)

app_name = "api"

urlpatterns = [
    path("login", views.UserLoginViewJWT.as_view()),
    path("", include(router.urls))
]
