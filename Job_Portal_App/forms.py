from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from Job_Portal_App.models import *

class RegisterForm(UserCreationForm):
    class Meta : 
        model = UserInfoModel
        fields = ["username", "display_name", "email", "user_types",'password1','password2']

    def __init__(self, *args, **kwargs):
        super( ).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})

class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})
