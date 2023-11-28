from django.contrib.auth import authenticate

from adminpanel.models import CustomUser
from providers.models import Provider

from .serializers import  (
    RegisterSerializer ,
    ProviderSerializer,    
    ProviderRegisterSerializer,
    UserSerializer
    )




from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['is_provider'] = user.is_provider
        # ...

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        reg_serilizer = RegisterSerializer(data=request.data)
        if reg_serilizer.is_valid():
            print('is____________valid')
            newuser = reg_serilizer.save()
            if newuser :
                print('user is created')
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serilizer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    
class ProviderRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def post(self, request , *args, **kwargs):
        reg_serilizer = ProviderRegisterSerializer(data=request.data)
        if reg_serilizer.is_valid():
            print("---------------------provider valid ------------------")
            newprov = reg_serilizer.save()
            if newprov :
                print('provider created')
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serilizer.errors , status=status.HTTP_400_BAD_REQUEST)