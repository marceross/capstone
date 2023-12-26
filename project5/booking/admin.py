from django.contrib import admin

from booking.models import User, UserProfile, Activity, ActivitySchedule, ActivityReservation

# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Activity)
admin.site.register(ActivitySchedule)
admin.site.register(ActivityReservation)

#, ActivityDays, ActivitySchedules, ActivityAttendance, ActivityScheduleSuspension, ActivityReservations, ActivityAutoReservation

#admin.site.register(ActivityDays)
#admin.site.register(ActivitySchedules)
#admin.site.register(ActivityAttendance)
#admin.site.register(ActivityScheduleSuspension)
#admin.site.register(ActivityReservations)
#admin.site.register(ActivityAutoReservation)