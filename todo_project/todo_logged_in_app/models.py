from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    length = models.IntegerField(default=60)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.title
