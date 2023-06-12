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
    restaurant             = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)

class Customer(models.Model):
    COMP = "Computing/JMC"
    MATH = "Math"
    BIOMED = "Bio-medical engineering"
    MEDICINE = "Medicine"

    DEPARTMENTS = [COMP, MATH, BIOMED, MEDICINE]

    DEPT_CHOICES = (
    (COMP, "Computing/JMC"),
    (MATH, "Math"),
    (BIOMED, "Bio-medical engineering"),
    (MEDICINE, "Medicine"),
    )

    name           = models.CharField(max_length=30)
    email          = models.EmailField(primary_key = True)
    is_student     = models.BooleanField(default=True, null=True)
    loyalty_points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    department     = models.CharField(max_length=30,
                        choices=DEPT_CHOICES,
                        default=COMP)

class Reservation(models.Model):
    order_no    = models.BigAutoField(primary_key = True)
    datetime    = models.DateTimeField(auto_now_add=True)
    meal        = models.ForeignKey(Meal, on_delete=models.CASCADE)
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    collected   = models.BooleanField(default=False)
