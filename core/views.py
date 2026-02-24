import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User


@login_required
def home_view(request):
    query = request.GET.get("q", "").strip()
    users = []

    memes = [
        "memes/meme1.png",
        "memes/meme2.png",
        "memes/meme3.png",
        "memes/meme4.png",
        "memes/meme5.png",
        "memes/meme6.png",
    ]

    random_meme = random.choice(memes)

    if query:
        users = User.objects.exclude(id=request.user.id).filter(
            Q(username__icontains=query) |
            Q(profile__full_name__icontains=query)
        )

    return render(
        request,
        "core/home.html",
        {
            "query": query,
            "users": users,
            "meme": random_meme
        }
    )