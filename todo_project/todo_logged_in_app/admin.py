from django.contrib import admin
from .models import Todo, TodoCatagory

# Register your models here.

admin.site.register(Todo)
admin.site.register(TodoCatagory)
