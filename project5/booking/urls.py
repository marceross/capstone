
from django.urls import path

from . import views

app_name = "booking"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("activitys", views.all_activitys, name="allactivitys"),

    path("create_activity", views.create_activity, name="create"),
    path('profile/<str:username>', views.user_profile_view, name='profile'),

    path("edit/<int:activity_id>", views.edit_activity, name="edit"),


]
'''path('follow_toggle/', views.follow_toggle, name='follow_toggle'),'''

'''path('following/<str:created_by>', views.following_activitys, name="following"),'''

'''path('/<username>', views.profile, name="profile"),'''
'''path('following/<str:username>', views.following, name="following"),'''

'''path('profile/<str:created_by>', views.user_profile_view, name='profile'),
REVERESE ERROR, TRYING TO FIX, SO WHEN CLICKING USER FROM A activity DIRECTS TO THAT USERS PROFILE
'''
