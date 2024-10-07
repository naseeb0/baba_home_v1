from . import views
from django.urls import path
from .views import SignUpView,LoginView,UserLogoutViewAPI,UserViewAPI, GetCsrfToken,UserUpdateView
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
    path('logout/',UserLogoutViewAPI.as_view(), name='logout'),
    path('user/', UserViewAPI.as_view(),name='user'),
    path('get-csrf-token/', GetCsrfToken.as_view(), name='get_csrf_token'),
    path('user/update/', UserUpdateView.as_view(), name='user-update'),
]