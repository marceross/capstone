from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"
    
class UserProfile(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_info')
    birthdate = models.DateField()
    photo = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=200)
    authorization = models.CharField(max_length=1)
    certificate = models.CharField(max_length=1)
    auto_reservation = models.BooleanField(null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following_users = models.ManyToManyField(User, blank=True, related_name="following_users")

    def __str__(self):
        return f"{self.user_profile} {self.birthdate}" 

class Activity(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_owner')
    activity_name = models.CharField(max_length=30)
    description = models.TextField()
    activity_image = models.CharField(max_length=200)
    active = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.name} {self.description}"