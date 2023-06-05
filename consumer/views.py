from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Meal
from django.core.handlers.wsgi import WSGIRequest
import json
import os

def media_view(request):
    file_name = os.path.join("media", request.GET.get('img'))
    return HttpResponse(open(file_name, "rb").read(), content_type="image/jpg")

def home_view(request):
    all_meals = Meal.objects.all()
    context = {
        "meals": all_meals
    }
    return render(request, 'home.html', context)

def reserve_success_view(request : WSGIRequest):
    if request.method == 'POST':
        try:    
            record = Meal.objects.get(meal_id = request.POST.get('meal_id'))
            record.number_of_reservations += 1
            record.save()
            return render(request, 'reserve_success.html', {"meal": record})
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