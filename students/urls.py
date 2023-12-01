from django.urls import path
from . import views

urlpatterns = [
    path('profile/' , views.profileView , name="stud-profile"),
    path('delete' , views.deleteAccount , name="stud-delete"),
]
