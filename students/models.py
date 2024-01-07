from django.db import models
from adminpanel.models import CustomUser
from django.utils import timezone
from providers.models import *
from adminpanel.models import *
import uuid


class Purchase(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    certified = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} purchased {self.course.name}"

    class Meta:
        unique_together = ("course", "student")


class PurchasedLesson(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_compelete = models.BooleanField(default=False, blank=True, null=True)
    is_watched = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.lesson} lesson for purchaser {self.purchase}"


class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    added_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.course} Review & Rating by {self.student}"


class Wishlist(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.course} wishlist by {self.student}"


class PaymentDetails(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    transaction = models.CharField(max_length=255, unique=True, blank=True)
    added_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self) -> str:
        return f"payment by {self.student.student.username}"


class EnrolledQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    passed = models.BooleanField(default=False)
    score_achieved = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.quiz} - Enrolled Quiz"
