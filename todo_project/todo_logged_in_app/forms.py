from django import forms
from .models import Todo, TodoCatagory


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'length', 'date', 'priority', 'catagory')

        labels = {
            'title': 'Title',
            'description': 'Description',
            'length': 'Length (minutes):',
       #     'date': 'Dateeee:',
        }


class CatagoryForm(forms.ModelForm):
    class Meta:
        model = TodoCatagory
        fields = ('name',)
