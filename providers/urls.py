from django.urls import path
from .views import UpdateProfile

urlpatterns = [
    path('profile-update' , UpdateProfile.as_view() , name="prov-update" ),
    path('profile' , UpdateProfile.as_view() , name="prov-profile" ),
]
