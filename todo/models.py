from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=500)  # todoリストの名前の長さ上限10000
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name
