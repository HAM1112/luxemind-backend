from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from .serializers import *
from rest_framework.decorators import api_view ,permission_classes
from .models import Provider
from adminpanel.models import CustomUser
from rest_framework.response import Response
from moviepy.video.io.VideoFileClip import VideoFileClip
# Create your views here.

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        provider = Provider.objects.get(id=user_id)
        serializer = ProfileSerializer(provider , data=request.data , partial=True)
        if serializer.is_valid():
            print('is valid')
            serializer.save()
            return Response({"message" : 'Updation Successful'})
        return Response(data={"message" : "Some erro has occured"})

    def get(self , request , *args, **kwargs):
        user_id = request.user.id
        provider = Provider.objects.get(id=user_id)
        serializer = ProfileSerializer(provider)
        print(serializer.data)
        return Response(data=serializer.data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def addCourse(request):
    mutable_data = request.data.copy()
    mutable_data['provider'] = request.user.pk
    serializer = CourseSerializer(data=mutable_data)
    if serializer.is_valid():
        serializer.save()
        return Response(data={"message" : "Course added successfully"}, status=201)
    else :
        print(serializer.errors)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def getAllCourses(request):
    provider = request.user.provider
    courses = Course.objects.filter(provider=provider)
    serializer = CourseSerializer(courses , many=True)
    return Response(data=serializer.data)
 
@api_view(['GET'])
@permission_classes([AllowAny])
def getAllSubjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects , many=True)
    return Response(data=serializer.data)
 
 
@api_view(['GET'])
# @permission_classes([AllowAny])
def getCourseDetails(request , course_id):
    course = Course.objects.get(id=course_id)
    provider = course.provider
    provider_serializer = ProfileSerializer(provider)
    course_serializer = CourseSerializer(course)
    print(course.subject.name)
    combined_data = {
        'provider': provider_serializer.data,
        'course': course_serializer.data,
        'subject' : course.subject.name
    }
    return Response(data=combined_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCourse(request , course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course , data=request.data , partial=True)
    if serializer.is_valid():
        print('yes working')
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addModule(request):
    print(request.data) 
    serializer = ModuleSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        course = serializer.validated_data['course']
        if not Module.objects.filter(name=name, course=course).exists():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Module with this name already exists for the given course.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addLesson(request):

    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        module = serializer.validated_data['module']
        
        lesson_url = serializer.validated_data['lesson_url']
        video_clip = VideoFileClip(lesson_url)
        duration = video_clip.duration
        minutes, seconds = divmod(duration, 60)
        duration_format = f"{int(minutes):02d}:{int(seconds):02d}"
        serializer.validated_data['lesson_duration'] = duration_format

        if not Lesson.objects.filter(name=name , module=module).exists():    
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'Lesson with this name already exists for the give module.'}, status=status.HTTP_400_BAD_REQUEST)
    print(serializer.errors)
    return Response(serializer.errors ,  status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurriculumDetails(request , course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=404)

    modules = Module.objects.filter(course=course)

    module_details = []
    for module in modules:
        module_serializer = ModuleSerializer(module)
        lessons = Lesson.objects.filter(module=module)
        lesson_serializer = LessonSerializer(lessons, many=True)
        module_detail = {
            'module': module_serializer.data,
            'lessons': lesson_serializer.data
        }
        module_details.append(module_detail)

    return Response(module_details)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_module(request, module_id):
    try:
        module = Module.objects.get(pk=module_id)
    except Module.DoesNotExist:
        return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)

    module.delete()
    return Response({'message': 'Module deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
    except Lesson.DoesNotExist:
        return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

    lesson.delete()
    return Response({'message': 'Lesson deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def publish_course(request , course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    if course.is_published:
        return Response({'error': 'Course is already published'}, status=status.HTTP_400_BAD_REQUEST)
    # course.is_published = True
    course.is_pending = True
    course.save()
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)