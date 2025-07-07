# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=150, blank=True, null=True)
#     about = models.TextField(blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta  # <-- import timedelta here

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    otp = models.CharField(max_length=6, null=True, blank=True)  # Uncommented
    otp_created_at = models.DateTimeField(null=True, blank=True)  # Uncommented

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def is_otp_valid(self, otp_input):
        return (
            self.otp == otp_input and
            self.otp_created_at and
            timezone.now() <= self.otp_created_at + timedelta(minutes=5)  # <-- use timedelta here
        )
