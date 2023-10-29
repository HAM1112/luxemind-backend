from django.db import models
from adminpanel.models import CustomUser
from django.utils import timezone


class Provider(CustomUser):
    education = models.CharField(max_length=100)
    storage_allocated = models.DecimalField(max_digits=5,decimal_places=1,default=2.0)
    rating = models.FloatField(default=0.0)