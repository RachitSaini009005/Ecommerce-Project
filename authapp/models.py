from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # phone_number = models.IntegerField()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # required for createsuperuser
    # REQUIRED_FIELDS = ['username','phone_number']  # required for createsuperuser