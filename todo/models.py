from django.db import models


class Post(models.Model):
    body = models.CharField(max_length=200)  # todoリストの名前の長さは200まで
