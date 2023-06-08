from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Meal, Reservation, Customer, Restaurant
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
import json
import os

email_subject = "Lets Solve Lunch! Order Confirmation"
email_id = "letssolvelunch@gmail.com"

def home_view(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        try:
            Customer.objects.get(email=user_email)
            request.session["user_email"] = user_email
        except Customer.DoesNotExist:
            return render(request, 'error_login.html', {})
 
    all_restaurants = Restaurant.objects.all()
    context = {
        "restaurants": all_restaurants
    }
    return render(request, 'home.html', context)

def emailsent_view(request : WSGIRequest):
    if request.POST.get('submit', None):
            order_no = (request.POST.get('submit'))
            reservation = Reservation.objects.get(order_no=order_no)
            meal = reservation.meal
            user_email = request.session['user_email']
            send_mail(email_subject,
            f"""Your order number is #{order_no} 
Meal Name: {meal.name}
Price: {meal.price_student}""", 
            email_id,
            [user_email] )
            return render(request, 'email_confirmation.html', {"email" : user_email})

def reserve_success_view(request : WSGIRequest):
    print(request.method)
    if request.method == 'POST':
    
        try:    
            meal = Meal.objects.get(meal_id = request.POST.get('meal_id'))
            meal.number_of_reservations += 1
            meal.save()

            # Make Reservation
            customer_email = request.session['user_email']
            print(request.session['user_email'])
            customer = Customer.objects.get(email=customer_email)
            reservation : Reservation = Reservation(meal=meal, customer=customer)
            reservation.save()

            return render(request, 'reserve_success.html', 
            {"meal": meal, "order_no" : reservation.order_no})
        
        except json.JSONDecodeError:
            return JsonResponse({"message" : "Reserve Unsuccessful"}, status=505)
    return JsonResponse({"message" : "Invalid Request Method"}, status=400) 

def confirm_reserve_view(request : WSGIRequest):
    print("here")
    if request.method == 'GET':
        try:    
            restaurant = Restaurant.objects.get(name = request.GET.get('restaurant'))
            meal : Meal = Meal.objects.get(meal_id = request.GET.get('meal_id'))
            return render(request, 'confirm_reserve.html', 
            {"meal_id" : meal.meal_id, "meal_name": meal.name, "meal_location" : restaurant})
        except json.JSONDecodeError:
            return JsonResponse({"message" : "Reserve Unsuccessful"}, status=505)

    return JsonResponse({"message" : "Invalid Request Method"}, status=400)     

def myaccount_view(request : WSGIRequest):
    user_email = request.session['user_email']
    customer : Customer = Customer.objects.get(email=user_email)
    reservations = Reservation.objects.filter(customer=customer)
    context = dict()

    # loyalty points and discount
    context["points"] = customer.loyalty_points
    context["discount"] = int(150 - ((customer.loyalty_points % 150)//7))

    if (len(reservations) > 0):
        reservation : Reservation = reservations.first() 
        meal : Meal = reservation.meal   
        context["reservation"] = True
        context["order_no"] = reservation.order_no
        context["meal_name"] = meal.name
    else:
        context["reservation"] = False
    context['customer_name'] = customer.name
    return render(request, 'myaccount.html', context)

def order_history_view(request):
    user_email = request.session['user_email']
    customer : Customer = Customer.objects.get(email=user_email)
    reservations = Reservation.objects.filter(customer=customer)
    context = {
        "reservations" : reservations
    }
    return render(request, 'order_history.html', context)

def restaurant_menu_view(request):
    restaurant = Restaurant.objects.get(name = request.GET.get('restaurant'))
    print(restaurant)       
    all_meals = Meal.objects.filter(restaurant = restaurant)
    # all_meals = Meal.objects.all()
    context = {
        "meals": all_meals,
        'restaurant': restaurant,
    }
    return render(request, 'restaurant_menu.html', context)

def leaderboard_view(request):
    context = dict()
    context['customers'] = sorted(list(Customer.objects.all()), key=lambda c : c.loyalty_points, reverse=True)
    context['current_customer_email'] = Customer.objects.get(email=request.session['user_email']).email
    return render(request, 'leaderboard.html', context)