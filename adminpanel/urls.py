from django.urls import path
from .views import *

urlpatterns = [
    path("profile/", AdminProfileView, name="admin-profile"),
    path("profile-update", UpdateProfileView.as_view(), name="admin-profile-update"),
    path("all-users/", listAllUsers, name="all-users"),
    path("update-status", updateUserStatus, name="update-status"),
    path("delete-user/<int:user_id>", deleteUser, name="delete-user"),
    path("get_all_courses/", get_all_courses, name="get_all_courses"),
    path("get_all_providers/", get_all_providers, name="get_all_providers"),
    path("approve_course/<int:course_id>", approver_course, name="approve_course"),
    path("block_course/<int:course_id>", block_course, name="block_course"),
    path("get_user_details/<int:user_id>/", get_user_details, name="user_details"),
]
