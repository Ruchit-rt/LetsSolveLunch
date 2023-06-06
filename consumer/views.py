from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Meal, Reservation
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
import json
import os

email_subject = "Lets Solve Lunch! Order Confirmation"
email_id = "letssolvelunch@gmail.com"

def media_view(request):
    file_name = os.path.join("media", request.GET.get('img'))
    return HttpResponse(open(file_name, "rb").read(), content_type="image/jpg")

def home_view(request):
    all_meals = Meal.objects.all()
    context = {
        "meals": all_meals
    }
    return render(request, 'home.html', context)

def emailsent_view(request):
    if request.POST.get('submit', None):
            order_no = (request.POST.get('submit'))
            reservation = Reservation.objects.get(order_no=order_no)
            meal = reservation.meal

            send_mail(email_subject,
f"""Your order number is #{order_no} 
Meal Name: {meal.name}
Price: {meal.price_student}""", email_id,['dj321@ic.ac.uk'] )
            return HttpResponse("Email Has Been Sent!")

def reserve_success_view(request : WSGIRequest):
    print(request.method)
    if request.method == 'POST':
    
        try:    
            meal = Meal.objects.get(meal_id = request.POST.get('meal_id'))
            meal.number_of_reservations += 1
            meal.save()

            # Make Reservation
            reservation : Reservation = Reservation(meal=meal)
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