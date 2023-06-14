from ast import Set
from taggit.models import Tag
import os
import json
import qrcode
from io import BytesIO
from main.models import Meal, Reservation, Customer, Restaurant
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files import File
from django.core.mail import EmailMessage
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from email.mime.image import MIMEImage

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
    tags = {}
    for meal in Meal.objects.all():
        for tag in meal.tags.all():
            tags[tag] = ""

    context['tags'] = list(tags.keys())
    return render(request, 'home.html', context)

def last_order_view(request):
    if request.POST.get('submit', None):
        order_no = (request.POST.get('submit'))
        reservation = Reservation.objects.get(order_no=order_no)
        return render(request, 'last_order.html', {'reservation': reservation})
    else:
        return render(request, 'last_order.html')



def emailsent_view(request : WSGIRequest):
    if request.POST.get('submit', None):
            order_no = (request.POST.get('submit'))
            reservation = Reservation.objects.get(order_no=order_no)
            image = reservation.qr
            meal = reservation.meal
            user_email = request.session['user_email']



            msg = EmailMessage(email_subject,
            f"""Your order number is #{order_no}<br> 
Meal Name: {meal.name}<br>
Price: {meal.price_student}<br><img src="cid:image"><br>""", 
            email_id,
            [user_email])
            msg.content_subtype = "html"
            att = MIMEImage(image.read())
            att.add_header('Content-ID', f'<image>')
            att.add_header('X-Attachment-Id', f'image.png')
            att['Content-Disposition'] = f'inline; filename=image.png'
            msg.attach(att)
            msg.send()
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
            customer = Customer.objects.get(email=customer_email)
            reservation : Reservation = Reservation(meal=meal, customer=customer)
            reservation.save()
            reservation.save()

            return render(request, 'reserve_success.html', 
            {"meal": meal, "order_no" : reservation.order_no, "meal_id" : meal.meal_id})
        
        except json.JSONDecodeError:
            return JsonResponse({"message" : "Reserve Unsuccessful"}, status=505)
    return JsonResponse({"message" : "Invalid Request Method"}, status=400) 

def confirm_reserve_view(request : WSGIRequest):
    if request.method == 'GET':
        try:    
            print(request.GET.get('restaurant'))
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
        reservation : Reservation = reservations.last() 
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
    rev_res = reversed(list(reservations))
    context = {
        "reservations" : rev_res
    }
    return render(request, 'order_history.html', context)

def restaurant_menu_view(request):
    restaurant = Restaurant.objects.get(name = request.GET.get('restaurant'))    
    all_meals = Meal.objects.filter(restaurant = restaurant)
    context = {
        "meals": all_meals,
        "restaurant": restaurant,
        "is_student" : Customer.objects.get(email=request.session.get('user_email')).is_student,
    }
    return render(request, 'restaurant_menu.html', context)

def leaderboard_view(request):
    context = dict()
    customers = sorted(list(Customer.objects.all()), key=lambda c : c.loyalty_points, reverse=True)
    context['customers'] = customers

    ranks = list(range(1,len(customers) + 1))
    names = map(lambda x: x.name,  customers)
    loyalty_points = map(lambda x: x.loyalty_points,  customers)
    departments = map(lambda x: x.department,  customers)
    emails = map(lambda x: x.email,  customers)
    context['LUnique'] = zip(ranks, names, loyalty_points, departments ,emails)

    context['current_customer_email'] = Customer.objects.get(email=request.session['user_email']).email
    return render(request, 'leaderboard.html', context)

def departmentLeaderBoard_view(request):
    context = dict()
    departments = Customer.objects.values('department').annotate(Sum('loyalty_points')).order_by('-loyalty_points__sum')

    ranks = list(range(1,len(departments) + 1))
    depts = [d['department'] for d in departments]
    loyalty_points = [d["loyalty_points__sum"] for d in departments]
    context['LUnique'] = zip(ranks, depts, loyalty_points)

    context['current_department'] = Customer.objects.get(email=request.session['user_email']).department
    return render(request, 'departmentLeaderBoard.html', context)

def tag_filter_view(request : WSGIRequest):
    context = dict()
    tag = request.GET.get('tag')
    context['tag'] = tag
    filtered_meals = Meal.objects.filter(tags__name__in=[tag])
    context['found'] = filtered_meals.count() > 0
    context['meals'] = filtered_meals
    context['is_student'] = Customer.objects.get(email=request.session.get('user_email')).is_student
    return render(request, 'tag_filter.html', context)