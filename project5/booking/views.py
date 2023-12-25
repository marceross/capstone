from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse

from django import forms

from .models import ActivitySchedule, User, UserProfile, Activity
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.core.serializers import serialize

from django.core.paginator import Paginator

class NewActivity(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ["active"]
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

''' 
is_following = False
def all_activitys(request):

    try:
        activitys = Activity.objects.order_by("-created_date").all()
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

            for activity in activitys:
                activity.is_following = user_profile.following_users.filter(username=activity.created_by.username).exists()
                    
        return render(request, 'booking/allactivitys.html', {'activitys': activitys, 'user_profile': user_profile, 'is_following': is_following})

    except Exception as e:
        print(f"Exception in all_activitys view: {e}")
        return render(request, 'booking/allactivitys.html', {'activitys': activitys})
'''

def all_activities(request):
    activities = Activity.objects.all()
    paginator = Paginator(activities, 5)
    if request.GET.get("page") != None:
        try:
            activities = paginator.page(request.GET.get("page"))
        except:
            activities = paginator.page(1)
    else:
        activities = paginator.page(1)
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


@login_required
def create_activity(request):
    if request.method== "POST":
        form = NewActivity(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            return  HttpResponseRedirect(reverse("booking:allactivitys"))
        else:
            return render(request, "booking/create_activity.html", {"form": form})
    return render(request, "booking/create_activity.html", {"form": NewActivity()})


@login_required
def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    if request.method == "POST":
        edit = NewActivity(request.POST, instance=activity)
        if edit.is_valid():
            edited_activity = edit.save(commit=False)
            edited_activity.save()
            return HttpResponseRedirect(reverse("booking:allactivitys"))
    else:
        edit = NewActivity(instance=activity)
        return render(request, "booking/create_activity.html", {"form": edit, "activity": activity})
    
@login_required
def following_activitys(request):
    # Get the current user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the list of users that the current user follows
    following_users = user_profile.following_users.all()

    # Get the activitys made by the users that the current user follows
    activitys = Activity.objects.filter(created_by__in=following_users).order_by("-created_date")

    return render(request, 'booking/following.html', {'activitys': activitys})



@require_POST
def like_activity(request, activity_id):
    user = request.user  
    if user.is_authenticated:
        activity = get_object_or_404(Activity, id=activity_id)

        # Check if the user has already liked the activity
        if user in activity.likes.all():
            # User has already liked the activity, handle this as needed
            activity.likes.remove(user)
            return redirect('booking:allactivitys')

        # Increment the like count and add the user to the likes
        activity.likes.add(user)
        activity.save()

        # Serialize the updated activity data
        activity_data = serialize('json', [activity])
        return redirect('booking:allactivitys')
    else:
        return redirect('booking:allactivitys')

    
def user_profile_view(request, username):
    if(request.user.is_authenticated):
        user = get_object_or_404(User, username=username)
        user_profile = UserProfile.objects.get(user=user)
        activitys = Activity.objects.filter(created_by=user).order_by('-created_date')
        current_profile = UserProfile.objects.get(user=request.user)
        followed = current_profile.following_users.filter(username=username).exists()
        print(followed)
        context = {
            'username':username,
            'user_profile': user_profile,
            'activitys': activitys,
            'followed': followed,
        }

        return render(request, 'booking/profile.html', context)
    else:
        login_url = reverse('booking:login')
        return redirect(login_url)


@login_required
def following_activitys(request):
    # Get the current user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Get the list of users that the current user follows
    following_users = user_profile.following_users.all()

    # Get the activitys made by the users that the current user follows
    activitys = Activity.objects.filter(created_by__in=following_users).order_by("-created_date")

    return render(request, 'booking/following.html', {'activitys': activitys})



@login_required
def follow_profile(request):
    if request.method == 'POST':
        created_by = request.POST.get('created_by')

        user_profile = get_object_or_404(UserProfile, user=request.user)
        to_follow_user, created = User.objects.get_or_create(username=created_by)
        to_follow_profile, created = UserProfile.objects.get_or_create(user=to_follow_user)

        if user_profile.following_users.filter(username=created_by).exists():
            user_profile.following_users.remove(to_follow_user)
            to_follow_profile.followers.remove(request.user)
        else:
            user_profile.following_users.add(to_follow_user)
            to_follow_profile.followers.add(request.user)

        return redirect('booking:profile', username=created_by)

    return redirect('booking:allactivitys')
