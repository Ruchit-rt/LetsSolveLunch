from django.shortcuts import render
from main.models import Meal

def mycafe_view(request):
    obj = Meal.objects.get(meal_id=1)
    context = dict()
    context['items'] = [{"name": meal.name, "number_of_reservations": meal.number_of_reservations} for meal in Meal.objects.all()]
    return render(request, 'mycafe.html', context)
