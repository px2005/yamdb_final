from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = ('email',)
