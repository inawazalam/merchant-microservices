from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Merchant


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Merchant
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Merchant
        fields = ('email',)
