from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("profile/", views.profileView, name="stud-profile"),
    path("update-profile/", updateProfie, name="update_profile"),
    path("delete", views.deleteAccount, name="stud-delete"),
    path(
        "get_all_published_courses/", get_all_published_courses, name="all_pub_courses"
    ),
    path("course_purchase", course_purchase, name="purchase course"),
    path("check_purchase/<int:course_id>/", check_purchased, name="purchase course"),
    path(
        "getCourseDetails/<int:course_id>/",
        purchased_course_details,
        name="purchase lesson",
    ),
    path("update_watched/<int:p_lesson_id>", update_lesson_watch, name="updatelesson"),
    path("update_complete/<int:p_lesson_id>", toggle_complete, name="updatecomplete"),
    path("enrolled/", get_enrolled_courses, name="enrolledCourses"),
    path("review-rating/", ReviewAndRating.as_view(), name="reveiw_rating"),
    path(
        "review-rating/<int:review_id>/",
        ReviewAndRating.as_view(),
        name="delete_rating",
    ),
    path("wishlist/", WishListView.as_view(), name="wishlist"),
    path("checkwishlist/<int:course_id>/", checkWishlist, name="check_wishlist"),
    path("course_payment/", payment_complete_course, name="complete-payment"),
    path("quiz-enroll", EnrollQuizView.as_view(), name="quiz-enroll"),
    path("all-certificate", certified_courses, name="course-certificates"),
]
