from django.forms import ModelForm

from .models import Post, Response


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'content']


class ResponseForm(ModelForm):

    class Meta:
        model = Response
        fields = ['text']
