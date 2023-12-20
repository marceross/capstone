from django.contrib import admin

from booking.models import User, UserProfile, Activity

# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Activity)


#, ActivityDays, ActivitySchedules, ActivityAttendance, ActivityScheduleSuspension, ActivityReservations, ActivityAutoReservation

#admin.site.register(ActivityDays)
#admin.site.register(ActivitySchedules)
#admin.site.register(ActivityAttendance)
#admin.site.register(ActivityScheduleSuspension)
#admin.site.register(ActivityReservations)
#admin.site.register(ActivityAutoReservation)