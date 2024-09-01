from django.urls import path
from .views import SignUpView, CustomTokenObtainPairView, CustomTokenRefreshView, UserViewAPI, UserLogoutViewAPI
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', UserLogoutViewAPI.as_view(), name='logout'),
    path('user/', UserViewAPI.as_view(), name='user'),
]