from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("upload-note/", views.upload_note, name="upload_note"),
    path("schedule/", views.schedule_meeting, name="schedule"),
    path("join/<int:meeting_id>/", views.join_meeting, name="join_meeting"),
    path("profile/", views.profile, name="profile"),
    path("chat/<int:user_id>/", views.chat, name="chat"),
    path("api/messages/<int:user_id>/", views.get_messages, name="get_messages"),
    path("users/", views.users_list, name="users_list"),
]



