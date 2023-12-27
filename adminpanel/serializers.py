from rest_framework.serializers import ModelSerializer
from .models import *
from providers.models import *
from students.models import *

class AdminSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class AdminProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name' , 'last_name')
        
class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
