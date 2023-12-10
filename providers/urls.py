from django.urls import path
from .views import *

urlpatterns = [
    path('profile-update' , UpdateProfile.as_view() , name="prov-update" ),
    path('profile' , UpdateProfile.as_view() , name="prov-profile" ),
    path('addCourse/' , addCourse  , name="addcourse" ),
    path('list-subjects/' , getAllSubjects  , name="getSubjects" ),
    path('list-courses/' , getAllCourses  , name="getCourses" ),
    path('getCourseDetails/<int:course_id>/' , getCourseDetails  , name="getCourseDetails" ),
    path('updateCourse/<int:course_id>' , updateCourse  , name="updateCourse" ),
    path('addModule/' , addModule , name="addModule" ),
    path('getCurriculumDetails/<int:course_id>/',getCurriculumDetails , name = "getCurriculumDetails" ),
    path('addLesson/' , addLesson , name="addLesson" ),
    path('delete_module/<int:module_id>/', delete_module, name='delete_module'),
    path('delete_lesson/<int:lesson_id>/', delete_lesson, name='delete_lesson'),
    path('publish_course/<int:course_id>', publish_course , name='publish_course'),
    
]
