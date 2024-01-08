from django.urls import path
from payments import views

urlpatterns = [
    path("save-stripe-info/", views.save_stripe_info, name="save_strip_info"),
]
