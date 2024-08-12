from . import views
from django.urls import path
from .views import SignUpView,LoginView,LogoutView,UserViewAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path("jwt/create",TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify", TokenVerifyView.as_view(), name="jwt_verify"),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('user/', UserViewAPI.as_view(),name='user')

]