from django.urls import path
from .views import  RegisterView , ProviderRegisterView , MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

urlpatterns = [
    # path('register/', CustomUserCreateView.as_view(), name='register'),
    
    path('studRegister/', RegisterView.as_view() , name='studregister'),
    path('provRegister/', ProviderRegisterView.as_view() , name='provregister'),
    
    # path('list/', ListCustomUser.as_view() , name='list'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
