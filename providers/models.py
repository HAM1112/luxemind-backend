from django.db import models
from adminpanel.models import CustomUser
from django.utils import timezone


class Provider(CustomUser):
    profession = models.CharField(max_length=100 , blank=True)
    storage_allocated = models.DecimalField(max_digits=5,decimal_places=1,default=2.0)
    rating = models.FloatField(default=0.0)
    about_me = models.TextField(blank=True)
    linked_in_link = models.CharField(max_length=255, unique=True , blank=True , null=True)
    insta_link = models.CharField(max_length=255, unique=True , blank=True , null=True)
    youtube_link = models.CharField(max_length=255, unique=True , blank=True , null=True)
    

class Subject(models.Model):
    name = models.CharField(max_length=255)


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    about = models.TextField()
    course_price = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_enrolls = models.PositiveIntegerField(blank=True , null=True)
    no_of_days = models.PositiveIntegerField(blank=True , null=True)
    certificate_url = models.URLField(blank=True, null=True)
    course_thumbnail = models.URLField(blank=True, null=True)
    course_preview = models.URLField(blank=True, null=True)
    level = models.CharField(max_length=50 ,blank=True , null=True)
    prerequisites = models.TextField(blank=True, null=True)
    no_of_views = models.PositiveIntegerField(default=0 , blank=True , null=True)
    is_published = models.BooleanField(default=False ,blank=True , null=True)
    is_pending = models.BooleanField(default=False ,blank=True , null=True)

    def __str__(self):
        return self.name
    
class Module(models.Model):
    name = models.CharField(max_length=255 )
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    index = models.PositiveIntegerField(blank=True, null=True)
    
    
    class Meta:
        unique_together = ('name', 'course')
    
class Lesson(models.Model):
    name = models.CharField(max_length=255 ,)
    module = models.ForeignKey(Module , on_delete=models.CASCADE)
    index = models.PositiveIntegerField(blank=True , null=True)
    lesson_url = models.URLField(blank=True, null=True)
    is_watched = models.BooleanField(default=False ,blank=True , null=True)
    is_completed = models.BooleanField(default=False ,blank=True , null=True)
    lesson_duration = models.CharField(max_length=8, blank=True, null=True)
    
    class Meta:
        unique_together = ('name' , 'module')
    
    def __str__(self):
        return self.name