from django.contrib.auth import authenticate

from adminpanel.models import CustomUser
from providers.models import Provider

from .serializers import  (
    RegisterSerializer ,
    ProviderSerializer,    
    ProviderRegisterSerializer,
    UserSerializer
    )

from .utils import create_jwt_pair_tokens

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import generics


class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                tokens = create_jwt_pair_tokens(user)
                refresh_token = RefreshToken(tokens['refresh'])
                serializer_user = None
                if user.is_provider:
                    real_user =  Provider.objects.get(email=email)
                    serializer_user = ProviderSerializer(real_user)
                else:
                    real_user = CustomUser.objects.get(email=email)
                    serializer_user = UserSerializer(real_user)
                response  = {
                    'message' : 'Login Successful',
                    "access_token": tokens['access'],
                    "refresh_token": tokens['refresh'],
                    "token_expiry": refresh_token['exp'],
                    'user' : serializer_user.data
                }
                
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response = {
                    "message" : "user is not verified"
                }
                return Response(data=response, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        else:
            print("there is an error")
            return Response(data={"message" : "Invalid email or password !"}, status=status.HTTP_400_BAD_REQUEST)
        

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