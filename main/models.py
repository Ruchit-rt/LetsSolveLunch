from datetime import datetime
from pyexpat import model
from django.db import models

# all models for LetsSolveLunch
class Restaurant(models.Model):
    name            = models.CharField(max_length=50)
    email           = models.EmailField(primary_key= True, max_length=254)
    open_time       = models.TimeField(auto_now_add=False)
    end_time        = models.TimeField(auto_now_add=False)

class Meal(models.Model):
    meal_id                = models.BigAutoField(primary_key = True)
    name                   = models.CharField(max_length=30)
    description            = models.CharField(max_length=200)
    picture                = models.ImageField(null=True, blank = True, upload_to="images/")
    number_of_reservations = models.IntegerField()
    price_staff            = models.DecimalField(max_digits=5, decimal_places=2)
    price_student          = models.DecimalField(max_digits=5, decimal_places=2)
    restaurant             = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Customer(models.Model):
    name    = models.CharField(max_length=30)
    email   = models.EmailField(primary_key = True)

class Reservation(models.Model):
    order_no    = models.BigAutoField(primary_key = True)
    datetime    = models.DateTimeField(auto_now_add=True)
    meal        = models.ForeignKey(Meal, on_delete=models.CASCADE)
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    collected   = models.BooleanField(default=False)
