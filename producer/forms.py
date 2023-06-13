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