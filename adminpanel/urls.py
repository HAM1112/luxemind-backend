from django.urls import path
from .views import (
    AdminProfileView , 
    UpdateProfileView , 
    listAllUsers,
    updateUserStatus,
    deleteUser,
)

urlpatterns = [
    path('profile/' ,AdminProfileView , name='admin-profile'),
    path('profile-update' , UpdateProfileView.as_view() , name='admin-profile-update'),
    path('all-users/', listAllUsers , name='all-users'),
    path('update-status', updateUserStatus , name='update-status'),
    path('delete-user/<int:user_id>', deleteUser , name='delete-user'),
]
