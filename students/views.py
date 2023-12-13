from django.shortcuts import render
from adminpanel.models import *
from .serializer import *
from providers.models import *
from providers.serializers import *


from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileView(request):
    user = request.user
    serializer = StudentProfileSerializer(user)
    print(serializer.data)
    return Response(data=serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteAccount(request):
    user = request.user
    user.delete()
    print('user deleted')
    return Response(data={"message" : "account deleted Successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_published_courses(request):
    courses = Course.objects.filter(is_published=True)
    serializer = CourseSerializer(courses , many=True)
    return Response(data=serializer.data)    