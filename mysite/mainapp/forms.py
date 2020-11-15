from django.forms import ModelForm
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Player,Tournament

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

class UserProfileForm(ModelForm):
    class Meta:
        model = Player
        # fields= '__all__'
        fields = ['phone','avatar']
        exclude = ['user']
        # fields = ['phone','avatar']
        widgets = {
            'avatar': forms.FileInput(),
        }

class CreateTour(ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'