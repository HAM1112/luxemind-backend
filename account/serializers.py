from rest_framework import serializers
from adminpanel.models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from providers.models import Provider

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ( 'email' , 'password', 'username')
        extra_kwargs = {'password' : {'write_only' : True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ProviderRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('username' , 'email'  ,  'password')
        extra_kwargs = {'password' : {'write_only' : True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_provider = True
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        exclude = ['password']