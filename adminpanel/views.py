from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from providers.models import *
from providers.serializers import *
from students.serializer import *
from .tasks import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def AdminProfileView(request):
    serializer = AdminSerializer(request.user)
    return Response(serializer.data)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = AdminProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "updated Successfully"})
        return Response()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listAllUsers(request):
    users = CustomUser.objects.exclude(pk=request.user.pk).order_by("id")
    serializer = AdminSerializer(users, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserStatus(request):
    user_id = request.data.get("id")
    user = CustomUser.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return Response(
        data={"message": "Status changed Successfully"}, status=status.HTTP_202_ACCEPTED
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteUser(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    users = CustomUser.objects.exclude(pk=request.user.pk).order_by("id")
    serializer = AdminSerializer(users, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(data=serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_providers(request):
    providers = Provider.objects.all()
    serializer = ProviderSerializer(providers, many=True)
    return Response(data=serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def approver_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    if course.is_published:
        return Response(
            {"error": "Course is already published"}, status=status.HTTP_400_BAD_REQUEST
        )
    course.is_pending = False
    course.is_published = True
    course.save()
    send_mail_to_related_students(course.subject.name, course.name)
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def block_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
    if not course.is_published:
        return Response(
            {"error": "Course is already Unpublished"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    course.is_pending = True
    course.is_published = False
    course.save()
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if user.is_provider:
        user = Provider.objects.get(id=user_id)
        serializer = ProviderSerializer(user)
        data = {
            "user": serializer.data,
        }
        return Response(data)

    serializer = UserSerializer(user)
    enrolled_courses = Course.objects.filter(purchase__student_id=user_id)
    payments = PaymentDetails.objects.filter(purchase__student=user)
    certifeid = Purchase.objects.filter(student=user, certified=True)

    all_payments = []
    for payment in payments:
        detials = {
            "payement": PayementDetailsSerializer(payment).data,
            "course": {
                "course_id": payment.purchase.course.id,
                "course_name": payment.purchase.course.name,
                "provider_id": payment.purchase.course.provider.id,
                "provider_name": payment.purchase.course.provider.username,
            },
        }
        all_payments.append(detials)

    data = {
        "user": serializer.data,
        "courses": CourseSerializer(enrolled_courses, many=True).data,
        "payments": all_payments,
        "certificates": PurchaseSerializer(certifeid, many=True).data,
    }
    return Response(data=data)


def test():
    print("physics")
    users = (
        CustomUser.objects.filter(purchase__course__subject__name="physics")
        .values_list("email", flat=True)
        .distinct()
    )
    print(users)
    return "what"
