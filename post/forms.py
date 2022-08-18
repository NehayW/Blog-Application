from dataclasses import fields
from django import forms
from .models import *


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['description', 'post_image']
