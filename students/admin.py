from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Purchase)
admin.site.register(PurchasedLesson)
admin.site.register(CourseRating)
admin.site.register(EnrolledQuiz)
admin.site.register(PaymentDetails)
