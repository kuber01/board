from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    TYPE = [
        ('Танки', 'tank'),
        ('Хилы', 'heal'),
        ('ДД', 'dd'),
        ('Торговцы', 'trader'),
        ('Гильдмастеры', 'guildmaster'),
        ('Квестгиверы', 'quest'),
        ('Кузнецы', 'smith'),
        ('Кожевники', 'tanner'),
        ('Зельевары', 'potion'),
        ('Мастера заклинаний', 'spellmaster')
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.CharField(max_length=20, choices=TYPE)
    date = models.DateTimeField(auto_now_add=True)
    content = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'
