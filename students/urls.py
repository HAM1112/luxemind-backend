from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('profile/' , views.profileView , name="stud-profile"),
    path('delete' , views.deleteAccount , name="stud-delete"),
    path('get_all_published_courses/' , get_all_published_courses , name='all_pub_courses'),
    
]
