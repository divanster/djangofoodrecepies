from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# from django.utils.translation import gettext as _
#
#
# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         labels = {
#             'username': _('Username'),
#             'email': _('Email'),
#             'password1': _('Password'),
#             'password2': _('Confirm pass'),
#         }


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput())
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
