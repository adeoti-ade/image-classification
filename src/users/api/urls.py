from django.urls import path, include

from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register(r'users', views.UserViewset)
# router.register(r"users", views.UserViewset, basename="user")

app_name = "api"

urlpatterns = [
    # path("create", views.UserCreateAPIView.as_view()),
    path("login", views.UserLoginViewJWT.as_view()),
    path("verify", views.EmailVerificationView.as_view()),
    path("", include(router.urls))
]

# urlpatterns += router.urls
