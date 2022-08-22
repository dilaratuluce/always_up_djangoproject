from django import forms
from .models import Todo, TodoCategory


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'length', 'date', 'priority', 'category')

        labels = {
            'title': 'Title',
            'description': 'Description',
            'length': 'Length (minutes):',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = TodoCategory
        fields = ('name',)
        labels = {
            'name': 'Name:',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '-'}),
        }
