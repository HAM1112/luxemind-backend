from django.urls import path
from .views import   Login , RegisterView , ProviderRegisterView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    # path('register/', CustomUserCreateView.as_view(), name='register'),
    path('login/', Login.as_view() , name='login'),
    path('studRegister/', RegisterView.as_view() , name='studregister'),
    path('provRegister/', ProviderRegisterView.as_view() , name='provregister'),
    
    # path('list/', ListCustomUser.as_view() , name='list'),
    
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
