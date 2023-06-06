from django.shortcuts import render
from main.models import Meal
from .forms import MealForm
from django.http import HttpResponseRedirect

def mycafe_view(request):
    obj = Meal.objects.get(meal_id=1)
    context = dict()
    context['items'] = [{"name": meal.name, "number_of_reservations": meal.number_of_reservations} for meal in Meal.objects.all()]
    return render(request, 'mycafe.html', context)

def add_menu_view(request):
    submitted = False
    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = MealForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'menu.html', {'form':form, 'submitted':submitted})
