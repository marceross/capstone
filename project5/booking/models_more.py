
class ActivityDays(models.Model):
    day_name = models.CharField(max_length=45, null=True)

    def __str__(self):
        return f"{self.day_name}" 

class ActivitySchedules(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_schedules')
    activity_day = models.ForeignKey(ActivityDays, on_delete=models.CASCADE, related_name='activity_schedules')
    time = models.TimeField(null=True)
    cost = models.IntegerField(null=True)
    capacity = models.IntegerField(null=True)
    specific_description = models.TextField(null=True)
    active = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.activity} {self.activity_day}" 

class ActivityAttendance(models.Model):
    user_attendance = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_attendance')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_attendance')
    dni = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user_attendance} {self.activity}" 

class ActivityScheduleSuspension(models.Model):
    activity_schedule_id_schedule = models.ForeignKey(ActivitySchedules, on_delete=models.CASCADE, related_name='schedule_suspensions')
    user_id = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.activity_schedule_id_schedule} {self.user_id}" 

class ActivityReservations(models.Model):
    user_reservation = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_reservations')
    date = models.DateField(null=True)
    activity_schedule_id_schedule = models.ForeignKey(ActivitySchedules, on_delete=models.CASCADE, related_name='activity_reservations')
    attend = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.user_reservation} {self.date}"

class ActivityAutoReservation(models.Model):
    user_auto = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auto_reservations')
    activity_schedule_id_schedule = models.ForeignKey(ActivitySchedules, on_delete=models.CASCADE, related_name='auto_reservations')

    def __str__(self):
        return f"{self.user_auto} {self.activity_schedule_id_schedule}"
        

'''
class Users(models.Model):
    id_user = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    user_type_id = models.IntegerField()
    active = models.CharField(max_length=1)

class UserTypes(models.Model):
    id_user_type = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=45)
'''
