from rest_framework import serializers
from adminpanel.models import CustomUser
from .models import Provider        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Provider
        fields = ('first_name' , "last_name" , 'dob' , 'education' , 'username' , 'email' )
    
        
    
    