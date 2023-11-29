from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class AdminSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class AdminProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name' , 'last_name')