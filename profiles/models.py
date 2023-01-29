from django.contrib.auth.models import User
from django.db import models


class Code(models.Model):
    number = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
