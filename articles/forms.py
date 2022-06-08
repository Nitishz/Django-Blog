from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'image')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Title Here'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Description Here'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})