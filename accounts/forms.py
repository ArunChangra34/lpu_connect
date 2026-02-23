from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

UNIVERSITY_DOMAIN = "@lpu.in"  # change later if needed

class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith(UNIVERSITY_DOMAIN):
            raise forms.ValidationError(
                "Please use your university email address."
            )
        return email
    


from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "department", "year", "bio", "interests"]
        widgets = {
            "interests": forms.CheckboxSelectMultiple(),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }




