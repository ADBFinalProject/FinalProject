from django.db import models
from django.utils import timezone


class User(models.Model):
    pseudo = models.CharField(max_length=30)
    summary = models.TextField()
    age = models.IntegerField()
    insertion_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.pseudo
