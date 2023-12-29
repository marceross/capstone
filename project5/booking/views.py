from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse

from django.http import HttpResponse

from django import forms

from .models import User, UserProfile, Activity, ActivitySchedule, ActivityReservation
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

from django.utils import timezone
from datetime import datetime, timedelta

class NewActivity(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ["created_by","active"]
        # Override the widget for the 'content' field
        widgets = {
            'activity': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        # Hide the label for the 'content' field
        labels = {
            'activity': '',
    }


def index(request):
    return render(request, "booking/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("booking:index"))
        else:
            return render(request, "booking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "booking/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("booking:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "booking/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "booking/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("booking:index"))
    else:
        return render(request, "booking/register.html")


def all_activities(request):
    activities = Activity.objects.all()
    return render(request, 'booking/all_activities.html', {'activities': activities})

def activity(request, activity_id):
    try:
        activity = Activity.objects.get(pk=activity_id)
    except activity.DoesNotExist:
        raise Http404("Activity not found.")
    return render(request, "booking/activity.html",
    {
        "activity": activity
    })

'''
@login_required
def schedule(request, schedule_id):
    message = ""
    try:
        schedule = ActivitySchedule.objects.get(pk=schedule_id)
        if request.method== "POST":
            if schedule.reservations.count() < schedule.capacity:
                schedule.reservations.add(request.user)
            else:
                message = "Exceded capacity"
    except schedule.DoesNotExist:
        raise Http404("schedule not found.")
    return render(request, "booking/schedule.html",
    {
        "schedule": schedule,
        "reserved": True if schedule.reservations.filter(activityreservation__user=request.user) else False,
        "message": message
    })
    '''


@login_required
def schedule(request, schedule_id):
    message = ""
    try:
        schedule = ActivitySchedule.objects.get(pk=schedule_id)
        user = request.user

        if request.method == "POST":
            # Check if the user has already made a reservation
            if schedule.reservations.filter(activityreservation__user=user).exists():
                # User wants to cancel the reservation
                schedule.reservations.remove(user)
                message = "Reservation canceled successfully."
            else:
                # User wants to make a new reservation
                if schedule.reservations.count() < schedule.capacity:
                    schedule.reservations.add(user)
                    message = "Reservation successful."
                else:
                    message = "Exceeded capacity"

    except ActivitySchedule.DoesNotExist:
        raise Http404("Schedule not found.")

    return render(request, "booking/schedule.html", {
        "schedule": schedule,
        "reserved": schedule.reservations.filter(activityreservation__user=user).exists(),
        "message": message
    })




@login_required
def create_activity(request):
    if request.method== "POST":
        form = NewActivity(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            return  HttpResponseRedirect(reverse("booking:all_activities"))
        else:
            return render(request, "booking/create_activity.html", {"form": form})
    return render(request, "booking/create_activity.html", {"form": NewActivity()})


@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    if request.method == "POST":
        '''edit = NewActivity(request.POST, instance=activity)
        if edit.is_valid():
            edited_activity = edit.save(commit=False)
            edited_activity.save()'''
        activity = request.POST.get('activity', '')  # 'activity' is the name attribute of the textarea
        activity.save()
        return HttpResponseRedirect(reverse("booking:all_activities"))
    else:
        edit = NewActivity(instance=activity)
        return render(request, "booking/create_activity.html", {"form": edit, "activity": activity})


@login_required
def user_profile_view(request, username):
    if(request.user.is_authenticated):
        #user = get_object_or_404(User, username=username)
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        #is_instructor = UserProfile.objects.get(user=user)
        activities = Activity.objects.filter(created_by=user).order_by()
        activities_schedule = ActivitySchedule.objects.filter(instructor=user)
        print()
        context = {
            'username':username,
            'user_profile': user_profile,
            'activitys': activities,
            'schedule': activities_schedule,
            #'followed': followed,
            #'is instructor':is_instructor,

        }

        return render(request, 'booking/profile.html', context)
    else:
        login_url = reverse('booking:login')
        return redirect(login_url)
    

#https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
@login_required
def edit_profile(request):
    if request.method == 'POST':
        #User.objects.get()
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'booking/edit_profile.html', {'form': form})


'''def see_agenda(request):
    current_user = request.user
    agendas = ActivityReservation.objects.filter(user=current_user)
    return render(request, 'booking/agenda.html', {'agendas': agendas})'''



def see_agenda(request):
    current_user = request.user
    agendas = ActivityReservation.objects.filter(user=current_user)

    if request.method == "POST":
        action = request.POST.get('action', '')
        schedule_id = request.POST.get('schedule_id')

        if action == "cancel":
            try:
                schedule = ActivitySchedule.objects.get(pk=schedule_id)
                # Make 'now' a timezone-aware datetime
                now = timezone.now()
                # Create a datetime object for the scheduled time on the current date
                scheduled_datetime = datetime.combine(now.date(), schedule.date.timetz())
                # Calculate the cancellation time limit (1 hour before the scheduled time)
                cancellation_time_limit = scheduled_datetime - timedelta(hours=1)
                if now < cancellation_time_limit:
                    # Display a warning message
                    message = "You can only cancel reservations more than one hour before the scheduled time."
                else:
                    # User is allowed to cancel the reservation
                    reservation = ActivityReservation.objects.get(user=current_user, schedule=schedule)
                    reservation.delete()
            except ActivitySchedule.DoesNotExist:
                raise Http404("Schedule not found.")
            except ActivityReservation.DoesNotExist:
                # Handle the case where the reservation does not exist
                pass
            # Redirect to the agenda page
            return redirect('booking:agenda')
    return render(request, 'booking/agenda.html', {'agendas': agendas})


def livesearch(request):
    output = ''
    query_param = request.GET.get('q', '')

    if query_param:
        results = Activity.objects.filter(nombre__icontains=query_param) | Activity.objects.filter(apellido__icontains=query_param)
    else:
        results = []

    if results:
        output += '<div class=""><table class="table-primary table-hover"><thead><tr><th>dni</th><th>nombre</th><th>apellido</th></tr></thead>'

        for result in results:
            output += f'''
                <tr>
                    <td><a href="app_vercliente2.py?id={result.dni}">{result.dni}</a></td>
                    <td>{result.nombre}</td>
                    <td>{result.apellido}</td>
                </tr>
            '''

        output += '</table></div>'
        return HttpResponse(output)