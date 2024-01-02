from rest_framework import serializers
from adminpanel.models import CustomUser
from .models import *       

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Provider
        fields = '__all__'
    

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Course
        fields = '__all__'

    def update(self, instance, validated_data):
        # Your custom update logic for nested fields
        nested_data = validated_data.pop('nested_field', None)
        if nested_data:
            # Your logic to update nested field
            pass
        # Continue with the regular update logic for other fields
        instance = super().update(instance, validated_data)

        return instance