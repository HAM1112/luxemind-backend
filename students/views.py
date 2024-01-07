from datetime import datetime, timedelta
from django.shortcuts import render
from adminpanel.models import *
from .serializer import *
from providers.models import *
from django.shortcuts import get_object_or_404
from providers.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import *


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profileView(request):
    user = request.user
    serializer = StudentProfileSerializer(user)
    print(serializer.data)
    return Response(data=serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfie(request):
    user = request.user
    print(request.data["first_name"])
    serializer = StudentProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteAccount(request):
    user = request.user
    user.delete()
    print("user deleted")
    return Response(data={"message": "account deleted Successfully"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_published_courses(request):
    courses = Course.objects.filter(is_published=True)
    serializer = CourseSerializer(courses, many=True)
    return Response(data=serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def course_purchase(request):
    course_id = request.data.get("id")  # Assuming you send the course ID in the request
    course = Course.objects.get(id=course_id)
    user = request.user
    today = datetime.now()
    date_of_expiration = today + timedelta(days=course.no_of_days)
    purchase_data = {
        "course": course_id,
        "student": user.id,
        "end_date": date_of_expiration,
    }
    serializer = PurchaseSerializer(data=purchase_data)
    if serializer.is_valid():
        instance = serializer.save()
        print(instance.id)
        course_instance = Course.objects.get(pk=course_id)
        lessons = Lesson.objects.filter(module__course=course_instance)
        for lesson in lessons:
            purchase_lesson = PurchasedLesson.objects.create(
                purchase=instance, lesson=lesson
            )

        return Response(serializer.data, status=201)
    return Response()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_purchased(request, course_id):
    course = Course.objects.get(id=course_id)
    user = request.user
    try:
        purchased = Purchase.objects.get(course=course, student=user)
        serializer = PurchaseSerializer(purchased)
        return Response(serializer.data)
    except Purchase.DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def purchased_course_details(request, course_id):
    course = Purchase.objects.get(course=course_id, student=request.user.id)
    lessons = PurchasedLesson.objects.filter(purchase=course)
    lesson_serializer = PurchasedLessonSerializer(lessons, many=True)
    return Response(lesson_serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_lesson_watch(request, p_lesson_id):
    p_lesson = PurchasedLesson.objects.get(id=p_lesson_id)
    p_lesson.is_watched = True
    p_lesson.save()
    return Response()


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_complete(request, p_lesson_id):
    p_lesson = PurchasedLesson.objects.get(id=p_lesson_id)
    p_lesson.is_compelete = not p_lesson.is_compelete
    p_lesson.save()
    return Response()


@api_view(["GET"])
@permission_classes([AllowAny])
def get_enrolled_courses(request):
    user = request.user
    purchases = Purchase.objects.filter(student=user)
    courses = []
    for purchase in purchases:
        purchase_serializer = PurchaseSerializer(purchase)
        course = Course.objects.get(id=purchase.course.id)
        p_lessons = PurchasedLesson.objects.filter(purchase=purchase)
        total_seconds = 0
        total_complete = 0
        for p_lesson in p_lessons:
            if p_lesson.lesson.lesson_duration:
                duration_parts = [
                    int(part) for part in p_lesson.lesson.lesson_duration.split(":")
                ]
                lesson_duration_timedelta = timedelta(
                    minutes=duration_parts[0], seconds=duration_parts[1]
                )
                total_seconds += lesson_duration_timedelta.total_seconds()
                if p_lesson.is_compelete:
                    dur_parts = [
                        int(part) for part in p_lesson.lesson.lesson_duration.split(":")
                    ]
                    less_duration_timedelta = timedelta(
                        minutes=dur_parts[0], seconds=duration_parts[1]
                    )
                    total_complete += less_duration_timedelta.total_seconds()
        total_duration = timedelta(seconds=total_seconds)
        total_comp = timedelta(seconds=total_complete)
        percentage = round(float((total_comp / total_duration) * 100), 1)
        course_serializer = CourseSerializer(course)
        data = {
            "purchase_details": purchase_serializer.data,
            "course_details": course_serializer.data,
            "total_length": str(total_duration),
            "complete_percentage": percentage,
        }
        courses.append(data)
    return Response(courses)


class ReviewAndRating(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        data["student"] = request.user.id
        if CourseRating.objects.filter(
            student=data["student"], course=data["course"]
        ).exists():
            return Response(
                {"error": "You have already submitted a review for this course."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CourseRatingSerializer(data=data)
        if serializer.is_valid():
            print("hello")
            serializer.save()
            return Response(
                {"success": "Review submitted successfully."},
                status=status.HTTP_201_CREATED,
            )
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = CourseRating.objects.get(id=review_id)
        if review.student != request.user:
            return Response(
                {"error": "You are not allowed to delete this review."},
                status=status.HTTP_403_FORBIDDEN,
            )
        review.delete()
        return Response(
            {"success": "Review deleted successfully."}, status=status.HTTP_200_OK
        )


class WishListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        student = request.user
        course_id = data["course_id"]
        if Wishlist.objects.filter(course=course_id, student=student.id).exists():
            wishlist = Wishlist.objects.get(course=course_id, student=student.id)
            wishlist.delete()
            return Response(
                {"message": "Removed from wishlist successfully", "fav": False}
            )
        course = Course.objects.get(id=course_id)
        wishlist = Wishlist.objects.create(course=course, student=student)
        wishlist.save()
        return Response({"message": "Added to wishlist Successfully", "fav": True})

    def get(self, request):
        student = request.user
        wishlists = Wishlist.objects.filter(student=student.id)
        data = []
        for wishlist in wishlists:
            course = Course.objects.get(id=wishlist.course.id)
            serializer = CourseSerializer(course)
            data.append(serializer.data)
        return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def checkWishlist(request, course_id):
    student = request.user.id
    if Wishlist.objects.filter(course=course_id, student=student).exists():
        return Response({"is_favorite": True})
    return Response({"is_favorite": False})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def payment_complete_course(request):
    data = request.data
    course_id = data.pop("course_id")
    purchased = Purchase.objects.get(student=request.user, course=course_id)
    amount = data["amount"]
    status = data["status"]
    transaction = data["transaction"]
    serializer = PayementDetailsSerializer(data=data)
    if serializer.is_valid():
        purchased.is_paid = True
        purchased.save()
        purchased_lessons = PurchasedLesson.objects.filter(purchase=purchased)
        purchased_lessons.update(is_watched=True)
        payment = PaymentDetails.objects.create(
            purchase=purchased, amount=amount, status=status, transaction=transaction
        )
        payment.save()
        return Response({"sucess": "upgraded course successfully"})
    return Response(serializer.error_messages)


class EnrollQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        student = data["student"]
        quiz = data["quiz"]
        if EnrolledQuiz.objects.filter(student=student, quiz=quiz).exists():
            enrolled_quiz = EnrolledQuiz.objects.get(student=student, quiz=quiz)
            serializer = EnrolledQuizSerializer(enrolled_quiz, data=data, partial=True)
        else:
            serializer = EnrolledQuizSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            if data["passed"] is True:
                purchased_course = Purchase.objects.get(
                    student=request.user, course=instance.quiz.course.id
                )
                purchased_course.certified = True
                purchased_course.save()
            return Response(serializer.data)
        return Response()

    def get(self, request):
        student = request.user
        enrolled_quizs = EnrolledQuiz.objects.filter(student=student)
        data = []
        for enrolled in enrolled_quizs:
            course_name = enrolled.quiz.course.name
            course_id = enrolled.quiz.course.id
            enrolled_serializer = EnrolledQuizSerializer(enrolled).data
            data.append(
                {
                    "enroll_quiz": enrolled_serializer,
                    "course": course_name,
                    "course_id": course_id,
                }
            )
        return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def certified_courses(request):
    user = request.user
    courses = Purchase.objects.filter(student=user, certified=True)
    courses_serializer_array = []
    for course in courses:
        course_serializer = CourseSerializer(course.course)
        courses_serializer_array.append(course_serializer.data)
    data = {
        "courses": courses_serializer_array,
        "student_name": f"{user.first_name} {user.last_name}",
    }

    return Response(data=data)
