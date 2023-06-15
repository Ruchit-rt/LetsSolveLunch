from django import forms
from django.forms import ModelForm
from main.models import Meal
from taggit.forms import *

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ("meal_id","name","description","picture","number_of_reservations","price_staff","price_student", "restaurant", "tags")
        exclude = ("restaurant",)
        m_tags = TagField()

        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-input'}),
            'description': forms.TextInput(attrs={'class': 'text-input'}),
            'picture': forms.FileInput(attrs={'class': 'text-input'}),
            'number_of_reservations': forms.NumberInput(attrs={'class': 'text-input'}),
            'price_staff': forms.NumberInput(attrs={'class': 'text-input'}),
            'price_student': forms.NumberInput(attrs={'class': 'text-input'}),
            'restaurant': forms.Select(attrs={'class': 'text-input'}),
            'tags': forms.TextInput(attrs={'class': 'text-input'})
        }