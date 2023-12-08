from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from providers.models import *
from providers.serializers import *


@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def AdminProfileView(request):
    serializer = AdminSerializer(request.user)
    return Response(serializer.data)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = AdminProfileUpdateSerializer(user, data=request.data , partial=True)
        print(user.first_name)
        if serializer.is_valid():
            print("serializer is valid")
            serializer.save()
            return Response(data={"message" : "updated Successfully"})
        else:
            print('not valid ')
        return Response()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listAllUsers(request):
    users = CustomUser.objects.exclude(pk=request.user.pk).order_by('id')
    serializer = AdminSerializer(users , many=True)
    return Response(data=serializer.data , status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserStatus(request):
    user_id = request.data.get('id')
    user = CustomUser.objects.get(id=user_id)
    print(user.is_active)
    user.is_active = not user.is_active
    print(user.username)
    print(user.is_active)
    user.save()
    return Response(data={'message' : 'Status changed Successfully'},status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request , user_id):
    print(user_id)
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    print('deleting user')
    users = CustomUser.objects.exclude(pk=request.user.pk).order_by('id')
    serializer = AdminSerializer(users , many=True)
    return Response(data=serializer.data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses , many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_providers(request):
    providers = Provider.objects.all()
    serializer = ProviderSerializer(providers , many=True)
    return Response(data=serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def approver_course(request , course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    if course.is_published:
        return Response({'error': 'Course is already published'}, status=status.HTTP_400_BAD_REQUEST)
    
    course.is_pending = False
    course.is_published = True
    course.save()
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
