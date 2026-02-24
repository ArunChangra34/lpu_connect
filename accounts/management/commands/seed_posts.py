from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Post
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed 20 random posts"

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR("No users found."))
            return

        sample_posts = [
            "Anyone going to the tech fest?",
            "Library is packed today 😅",
            "Who wants to join the AI club?",
            "Cafeteria food hit different today.",
            "Group study tonight?",
            "Mid sems are coming 😭",
            "Just finished my ML assignment!",
            "Football match at 6pm ⚽",
            "Hostel life is chaotic.",
            "Best prof in CSE department?",
            "Anyone preparing for placements?",
            "Hackathon this weekend!",
            "Who’s attending the cultural night?",
            "Campus looks beautiful today.",
            "Need notes for DBMS.",
            "Exam schedule out yet?",
            "Morning lectures are a crime.",
            "New coffee machine is amazing.",
            "Working on a startup idea 👀",
            "Coding till 3AM again."
        ]

        for content in sample_posts:
            user = random.choice(users)
            Post.objects.create(user=user, content=content)

        self.stdout.write(self.style.SUCCESS("20 random posts created!"))