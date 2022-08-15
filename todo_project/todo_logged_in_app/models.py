from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField

from datetime import timedelta, date
from django import forms
# Create your models here.

from django.contrib.auth import get_user_model

DATE_CHOICES = (
    (datetime.date.today(), datetime.date.today()),
    (datetime.date.today() + timedelta(days=1), datetime.date.today() + timedelta(days=1)),
    (datetime.date.today() + timedelta(days=2), datetime.date.today() + timedelta(days=2)),
    (datetime.date.today() + timedelta(days=3), datetime.date.today() + timedelta(days=3)),
    (datetime.date.today() + timedelta(days=4), datetime.date.today() + timedelta(days=4)),
    (datetime.date.today() + timedelta(days=5), datetime.date.today() + timedelta(days=5)),
    (datetime.date.today() + timedelta(days=6), datetime.date.today() + timedelta(days=6)),

)

PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('normal', 'Normal'),
    ('high', 'High'),
    ('very_high', 'Very high')
)


"""
class Catagory(models.Model):
    name = models.CharField(choices=CATAGORY_CHOICES, max_length=100, default='-')
"""
#Catagory_choices = ()
#for catagory in TodoCatagory.objects.all():
#    Catagory_choices = Catagory_choices + {"catagory.name": catagory.name})

#CATAGORY_CHOICES = Catagory_choices


class TodoCatagory(models.Model):
    name = models.CharField(max_length=100, default='-')
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    length = models.IntegerField(default=60)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    priority = models.TextField(choices=PRIORITY_CHOICES, default='normal')
    catagory = models.ForeignKey(TodoCatagory, max_length=100, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


    # kendi eklediği kategori, kategori seç ya da kendin ekle, jquery select2 kütüphanesi kullanabilirsin


#   catagory = models.ForeignKey(TodoCatagory, max_length=100, on_delete=models.CASCADE, blank=True, null=True)

