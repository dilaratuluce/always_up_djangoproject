from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'length', 'date')

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
