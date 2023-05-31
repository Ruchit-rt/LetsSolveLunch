from django.shortcuts import render
from main.models import Meal

def mycafe_view(request):
    obj = Meal.objects.get(meal_id=1)
    context = {
        "num_reservations": obj.number_of_reservations
    }
    return render(request, 'mycafe.html', context)
