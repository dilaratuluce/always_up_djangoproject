from django import forms
from .models import Todo, TodoCatagory


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'length', 'date', 'priority')

        labels = {
            'title': 'Title',
            'description': 'Description',
            'length': 'Length (minutes):',
       #     'date': 'Dateeee:',
        }

     #   widgets = {
         #   'title': forms.TextInput(attrs={'class': 'form-control'}),
          #  'description': forms.TextInput(attrs={'class': 'form-control'}),
           # 'length': forms.NumberInput(attrs={'class': 'form-control'}),
        #    'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
     #   }


class CatagoryForm(forms.ModelForm):
    class Meta:
        model = TodoCatagory
        fields = ('name',)
