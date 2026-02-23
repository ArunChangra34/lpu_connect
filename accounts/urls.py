from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup_view
from .views import profile_view, edit_profile
from .views import ( users_list,send_request,friend_requests, accept_friend_request,)
from .views import chat_view
from .views import user_profile_view, conversations_view, friend_requests

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", LoginView.as_view(
        template_name="accounts/login.html"
    ), name="login"),
    path(
    "logout/",
    LogoutView.as_view(next_page="signup"),
    name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("users/", users_list, name="users_list"),
    path("friend-requests/", friend_requests, name="friend_requests"),
    path("request/send/<int:user_id>/",send_request,name="send_request"),
    path("friend-request/accept/<int:request_id>/", accept_friend_request, name="accept_request"),
    path("chat/<int:user_id>/", chat_view, name="chat"),
    path("user/<int:user_id>/", user_profile_view, name="user_profile"),
    path("messages/", conversations_view, name="messages"),
    path("requests/", friend_requests, name="requests"),
]






