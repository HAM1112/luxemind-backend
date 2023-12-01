from rest_framework import serializers
from adminpanel.models import CustomUser

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name' , 'last_name' , 'dob' , 'email' ,'date_joined' , 'username' ,'avatar')
        
    