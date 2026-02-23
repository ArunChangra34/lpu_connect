from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentSignupForm
from django.db import models

def signup_view(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = StudentSignupForm()

    return render(request, "accounts/signup.html", {"form": form})


from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def profile_view(request):
    profile = request.user.profile

    following = Follow.objects.filter(
        follower=request.user
    )

    followers = Follow.objects.filter(
        following=request.user
    )

    requests = Request.objects.filter(
        to_user=request.user
    )
    request_count = Request.objects.filter(
    to_user=request.user
    ).count()

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "following": following,
            "followers": followers,
            "requests": requests,
            "request_count": request_count,
        }
    )



@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Request, Follow, User


@login_required
def send_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    if to_user != request.user:
        Request.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

    return redirect("home")


@login_required
def friend_requests(request):
    requests = request.user.received_requests.all()
    return render(
        request,
        "accounts/friend_requests.html",
        {"requests": requests}
    )



@login_required
def accept_friend_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    if req.to_user == request.user:
        Follow.objects.get_or_create(
            follower=req.from_user,
            following=req.to_user
        )
        req.delete()

    return redirect("profile")

from django.db.models import Q
from .models import User, Request, Follow

@login_required
def users_list(request):
    query = request.GET.get("q", "")
    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(profile__full_name__icontains=query)
        )

    # Exclude users you already sent requests to
    sent_requests = Request.objects.filter(
        from_user=request.user
    ).values_list("to_user_id", flat=True)

    users = users.exclude(id__in=sent_requests)

    return render(
        request,
        "accounts/users_list.html",
        {"users": users, "query": query}
    )


from .models import Message, Conversation


def is_mutual_follow(user1, user2):
    return (
        Follow.objects.filter(follower=user1, following=user2).exists()
        and
        Follow.objects.filter(follower=user2, following=user1).exists()
    )


@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if not is_mutual_follow(request.user, other_user):
        return redirect("home")

    # Ensure consistent order
    user1, user2 = sorted([request.user, other_user], key=lambda x: x.id)

    conversation, created = Conversation.objects.get_or_create(
        user1=user1,
        user2=user2
    )

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
        return redirect("chat", user_id=other_user.id)

    messages = conversation.messages.all().order_by("timestamp")

    return render(
        request,
        "accounts/chat.html",
        {
            "conversation": conversation,
            "messages": messages,
            "other_user": other_user,
        }
    )

@login_required
def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile

    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()

    is_followed_by = Follow.objects.filter(
        follower=user,
        following=request.user
    ).exists()

    is_mutual = is_following and is_followed_by

    has_requested = Request.objects.filter(
        from_user=request.user,
        to_user=user
    ).exists()

    is_self = request.user == user

    return render(
        request,
        "accounts/user_profile.html",
        {
            "profile_user": user,
            "profile": profile,
            "followers": followers,
            "following": following,
            "is_following": is_following,
            "is_mutual": is_mutual,
            "has_requested": has_requested,
            "is_self": is_self,
        }
    )

@login_required
def conversations_view(request):
    conversations = Conversation.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    )

    return render(
        request,
        "accounts/conversations.html",
        {"conversations": conversations}
    )
