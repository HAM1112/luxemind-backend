from rest_framework import serializers
from adminpanel.models import CustomUser
from .models import *
from adminpanel.serializers import *


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class PurchasedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedLesson
        fields = "__all__"


class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = "__all__"


class DisplayRatingSerializer(serializers.ModelSerializer):
    student = UserSerializer()

    class Meta:
        model = CourseRating
        fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"


class PayementDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        depth = 3
        fields = "__all__"


class EnrolledQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledQuiz
        fields = "__all__"
