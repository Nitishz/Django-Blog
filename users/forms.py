from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=25, required=True)
    last_name = forms.CharField(max_length=25, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['first_name'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'type': 'email', 'class': 'form-control', 'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update({'type': 'password', 'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'type': 'password', 'class': 'form-control', 'placeholder': 'Confirm password'})

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'type': 'password', 'class': 'form-control', 'placeholder': 'Enter password'})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['first_name'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'type': 'email', 'class': 'form-control', 'placeholder': 'Enter Email'})