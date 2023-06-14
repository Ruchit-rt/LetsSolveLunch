from ast import Set
from django.shortcuts import render
from django.http import JsonResponse
from taggit.models import Tag
from main.models import Meal, Reservation, Customer, Restaurant
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
import json
from django.db.models import Sum

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
    customers = sorted(list(Customer.objects.all()), key=lambda c : c.loyalty_points, reverse=True)
    context['customers'] = customers

    ranks = list(range(1,len(customers) + 1))
    names = map(lambda x: x.name,  customers)
    loyalty_points = map(lambda x: x.loyalty_points,  customers)
    departments = map(lambda x: x.department,  customers)
    emails = map(lambda x: x.email,  customers)
    context['LIndiUnique'] = zip(ranks, names, loyalty_points, departments ,emails)
    
    dpt_departments = Customer.objects.values('department').annotate(Sum('loyalty_points')).order_by('-loyalty_points__sum')
    dpt_ranks = list(range(1,len(dpt_departments) + 1))
    dpt_depts = [d['department'] for d in dpt_departments]
    dpt_loyalty_points = [d["loyalty_points__sum"] for d in dpt_departments]
    context['LDeptUnique'] = zip(dpt_ranks, dpt_depts, dpt_loyalty_points)
    context['current_department'] = Customer.objects.get(email=request.session['user_email']).department

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
    context = {}
    tag = request.GET.get('tag')
    context['tag'] = tag
    filtered_meals = Meal.objects.filter(tags__name__in=[tag])
    context['found'] = filtered_meals.count() > 0
    # print(filtered_meals)
    context['meals'] = filtered_meals
    return render(request, 'tag_filter.html', context)