from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User

@login_required
def home_view(request):
    query = request.GET.get("q", "").strip()
    users = []

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
            "users": users
        }
    )