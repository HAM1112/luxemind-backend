from rest_framework import serializers
from adminpanel.models import CustomUser

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


    