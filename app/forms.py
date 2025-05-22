from django.contrib.auth.forms import UserChangeForm, UserCreationForm


from .models import CustomUserModel

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUserModel
        fields = "__all__"

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUserModel
        fields = "__all__"
        