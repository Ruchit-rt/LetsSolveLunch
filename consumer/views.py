from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Meal, Reservation, Customer
from django.core.handlers.wsgi import WSGIRequest
import json
import os

def media_view(request):
    file_name = os.path.join("media", request.GET.get('img'))
    return HttpResponse(open(file_name, "rb").read(), content_type="image/jpg")

def home_view(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        try:
            Customer.objects.get(email=user_email)
            request.session["user_email"] = user_email
        except Customer.DoesNotExist:
            return render(request, 'error_login.html', {})
 
    all_meals = Meal.objects.all()
    context = {
        "meals": all_meals
    }
    return render(request, 'home.html', context)

def reserve_success_view(request : WSGIRequest):
    if request.method == 'POST':
        try:    
            meal = Meal.objects.get(meal_id = request.POST.get('meal_id'))
            meal.number_of_reservations += 1
            meal.save()

            # Make Reservation
            customer_email = request.session['user_email']
            customer = Customer.objects.get(email=customer_email)
            reservation : Reservation = Reservation(meal=meal, customer=customer)
            reservation.save()

            return render(request, 'reserve_success.html', 
            {"meal": meal, "order_no" : reservation.order_no})
        
        except json.JSONDecodeError:
            return JsonResponse({"message" : "Reserve Unsuccessful"}, status=505)

    return JsonResponse({"message" : "Invalid Request Method"}, status=400) 

def confirm_reserve_view(request : WSGIRequest):
    if request.method == 'GET':
        try:    
            meal : Meal = Meal.objects.get(meal_id = request.GET.get('meal_id'))
            return render(request, 'confirm_reserve.html', 
            {"meal_id" : meal.meal_id, "meal_name": meal.name, "meal_location" : "SCR"})
        except json.JSONDecodeError:
            return JsonResponse({"message" : "Reserve Unsuccessful"}, status=505)

    return JsonResponse({"message" : "Invalid Request Method"}, status=400)     

def myaccount_view(request : WSGIRequest):
    user_email = request.session['user_email']
    customer : Customer = Customer.objects.get(email=user_email)
    reservations = Reservation.objects.filter(customer=customer)
    context = dict()

    context["lol"]  = "lol"

    if (len(reservations) > 0):
        reservation : Reservation = reservations.first() 
        meal : Meal = reservation.meal   
        context["reservation"] = True
        context["order_no"] = reservation.order_no
        context["name"] = meal.name
    else:
        context["reservation"] = False

    return render(request, 'myaccount.html', context)

def order_history_view(request):
    user_email = request.session['user_email']
    customer : Customer = Customer.objects.get(email=user_email)
    reservations = Reservation.objects.filter(customer=customer)
    context = {
        "reservations" : reservations
    }
    return render(request, 'order_history.html', context)