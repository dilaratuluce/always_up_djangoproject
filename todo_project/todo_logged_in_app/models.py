from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField

from datetime import timedelta, date
from django import forms
# Create your models here.

DATE_CHOICES = (
    (datetime.date.today(), datetime.date.today()),
    (datetime.date.today() + timedelta(days=1), datetime.date.today() + timedelta(days=1)),
    (datetime.date.today() + timedelta(days=2), datetime.date.today() + timedelta(days=2)),
    (datetime.date.today() + timedelta(days=3), datetime.date.today() + timedelta(days=3)),
    (datetime.date.today() + timedelta(days=4), datetime.date.today() + timedelta(days=4)),
    (datetime.date.today() + timedelta(days=5), datetime.date.today() + timedelta(days=5)),
    (datetime.date.today() + timedelta(days=6), datetime.date.today() + timedelta(days=6)),

)


class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField(blank=True, null=True)
    length = models.IntegerField(default=60)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateField(choices=DATE_CHOICES, blank=True, default=datetime.date.today)

    def __str__(self):
        return self.title


    #kendi eklediği kategori, kategori seç ya da kendin ekle, jquery select2 kütüphanesi kullanabilirsin
