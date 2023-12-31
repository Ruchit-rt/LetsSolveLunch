import decimal
from datetime import datetime, timezone
from decimal import Decimal

from django.core.handlers.wsgi import WSGIRequest
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from main.models import Customer, Meal, Reservation, Restaurant

from .forms import MealForm


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
    context['meals'] = all_meals
    return render(request, 'mycafe.html', context)

def menu_view(request):
    if request.method == "POST":
        if request.POST.get("delete"):
            delete_item_id = request.POST.get("delete")
            Meal.objects.filter(meal_id = delete_item_id).delete()
            print(delete_item_id)
    producer_email = request.session["producer_email"]
    restaurant = Restaurant.objects.get(email=producer_email)
    all_meals = Meal.objects.filter(restaurant = restaurant)
    context = {
        "meals": all_meals,
        "restaurant_name": restaurant.name
    }
    return render(request, 'displaymenu.html', context)

def edit_menu_view(request):
    menu_id = request.GET.get("edit")
    old_meal = Meal.objects.get(meal_id=menu_id)
    form =  MealForm(request.POST or None, instance=old_meal)
    if form.is_valid():
        form.save()
        
        return redirect('../displaymenu/')
    print(menu_id)
    return render(request, 'edit_menu.html', {'meal':old_meal, 'form': form})

def add_menu_view(request):
    submitted = False
    producer_email = request.session["producer_email"]
    restaurant = Restaurant.objects.get(email=producer_email)
    if request.method == "POST":
        form = MealForm(request.POST, request.FILES, initial={'number_of_reservations': 0, 'restaurant': restaurant})
        if form.is_valid():
            m_tags = form.cleaned_data['tags']
            # object.tags.add(*m_tags)
            formcopy = form.save(commit=False)
            formcopy.restaurant = restaurant
            formcopy.save()
            form.save_m2m()
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