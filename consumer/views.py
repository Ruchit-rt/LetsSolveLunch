from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Meal
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def reserve_view(request):
    if request.method == 'POST':
        try:    
            data = json.loads(request.body)

            record = Meal.objects.get(meal_id=data['meal_id'])
            record.number_of_reservations += 1
            record.save()
            return JsonResponse({"message" : "Reserve Successful"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message" : "Reserve Unsuccessful"}, status=505)

    return JsonResponse({"message" : "Invalid Request Method"}, status=400)     