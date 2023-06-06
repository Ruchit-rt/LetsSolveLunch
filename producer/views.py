from datetime import datetime, timezone
from multiprocessing import context
from django.shortcuts import render
from .forms import MealForm
from django.http import HttpResponseRedirect
from main.models import Meal, Reservation
from django.core.handlers.wsgi import WSGIRequest

def mycafe_view(request):
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

def checkout_view(request):
    return render(request, 'checkout.html', {})

def checkout_result_view(request : WSGIRequest):
    context = {"message" : "Well this is awkward. Please enter order number correctly."}
    try:
        reservation : Reservation = Reservation.objects.get(order_no=request.POST.get("order_no"))
        date_diff = (datetime.now(timezone.utc) - reservation.datetime).days
        if date_diff == 1 or date_diff == 0:
            if not reservation.collected:
                reservation.collected = True
                reservation.save()
                return render(request, 'checkout_success.html', {})
            else:
                context["message"] = "Duplicate collection."
        else:
            context["message"] = "Order date expired."
        return render(request, 'checkout_failure.html', context)
    except Reservation.DoesNotExist:
        return render(request, 'checkout_failure.html', context)
