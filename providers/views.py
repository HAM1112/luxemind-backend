from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from .serializers import ProfileSerializer
from .models import Provider
from adminpanel.models import CustomUser
from rest_framework.response import Response
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