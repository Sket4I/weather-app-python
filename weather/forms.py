from turtle import width
from .models import City
from django.forms import ModelForm, TextInput

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={
            'class': 'form-control mt-md-1', 
            'name': 'city', 
            'id': 'city',
            'placeholder': 'Введите название города'
        })}
