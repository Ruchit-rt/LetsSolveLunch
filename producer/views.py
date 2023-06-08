from datetime import datetime, timezone
from decimal import Decimal
import decimal
from django.shortcuts import render
from .forms import MealForm
from django.http import HttpResponseRedirect
from main.models import Customer, Meal, Reservation, Restaurant
from django.core.handlers.wsgi import WSGIRequest

def mycafe_view(request):
    if request.method == "POST":
        producer_email = request.POST.get("producer_email")
        request.session["producer_email"] = producer_email
        try:
            restaurant = Restaurant.objects.get(email=producer_email)
        except Restaurant.DoesNotExist:
            return render(request, "email_error.html", {})
    all_meals = Meal.objects.filter(restaurant = Restaurant.objects.get(email=request.session["producer_email"]))
    context = dict()
    context['items'] = [{"name": meal.name, "number_of_reservations": meal.number_of_reservations} for meal in all_meals]
    return render(request, 'mycafe.html', context)

def menu_view(request):
    producer_email = request.session["producer_email"]
    restaurant = Restaurant.objects.get(email=producer_email)
    all_meals = Meal.objects.filter(restaurant = restaurant)
    context = {
        "meals": all_meals,
        "restaurant_name": restaurant.name
    }
    return render(request, 'displaymenu.html', context)

def add_menu_view(request):
    submitted = False
    producer_email = request.session["producer_email"]
    restaurant = Restaurant.objects.get(email=producer_email)
    if request.method == "POST":
        form = MealForm(request.POST, request.FILES, initial={'restaurant': restaurant})
        if form.is_valid():
            formcopy = form.save(commit=False)
            formcopy.restaurant = restaurant
            formcopy.save()
            return HttpResponseRedirect('?submitted=True')
    else:
        form = MealForm
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form':form, 
        'submitted':submitted
    }

    return render(request, 'menu.html', context)

def checkout_view(request):
    return render(request, 'checkout.html', {})

def checkout_result_view(request : WSGIRequest):
    context = {"message" : "Well this is awkward. Please enter order number correctly."}
    try:
        reservation : Reservation = Reservation.objects.get(order_no=request.POST.get("order_no"))
        date_diff = (datetime.now(timezone.utc) - reservation.datetime).days
        if date_diff == 1 or date_diff == 0:
            if not reservation.collected:
                if reservation.meal.restaurant.email == request.session["producer_email"]:
                    reservation.collected = True                
                    reservation.save()

                    # increment loyalty points for customers
                    customer : Customer = reservation.customer
                    points = 0
                    if (customer.is_student):
                        points += reservation.meal.price_student
                    else:
                        points += reservation.meal.price_staff
                    customer.loyalty_points += decimal.Decimal(points)
                    customer.save()
                    return render(request, 'checkout_success.html', {"points" : str(points)})
                else:
                    context["message"] = "Incorrect reservation location"
            else:
                context["message"] = "Duplicate collection."
        else:
            context["message"] = "Order date expired."
        return render(request, 'checkout_failure.html', context)
    except Reservation.DoesNotExist:
        return render(request, 'checkout_failure.html', context)
