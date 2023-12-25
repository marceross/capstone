from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    birthdate = models.DateField()
    photo = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=200)
    authorization = models.CharField(max_length=1)
    certificate = models.CharField(max_length=1)
    auto_reservation = models.BooleanField(null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following_users = models.ManyToManyField(User, blank=True, related_name="following_users")
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.birthdate}" 

class Activity(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_owner')
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.description}"

class ActivitySchedule(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_activities')
    date = models.DateTimeField(null=True)
    capacity = models.IntegerField(null=True)
    cost = models.IntegerField(null=True)
    description = models.TextField(null=True)
    active = models.BooleanField(default=True)
    reservations = models.ManyToManyField(User, through='ActivityReservation')

    def __str__(self):
        return f"{self.activity} {self.date}"

class ActivityReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(ActivitySchedule, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=True, default=timezone.now)

    def __str__(self):
        return f"{self.timestamp} {self.user} {self.timestamp}"

class ActivityAttendance(models.Model):
    user_attendance = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_attendance')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_attendance')
    dni = models.CharField(max_length=10)
    timestamp = models.DateTimeField(null=True, default=timezone.now)
    attended = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_attendance} {self.activity}"