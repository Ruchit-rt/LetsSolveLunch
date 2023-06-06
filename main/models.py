from datetime import datetime
from pyexpat import model
from django.db import models

# all models for LetsSolveLunch
class Meal(models.Model):
    meal_id                = models.BigAutoField(primary_key = True)
    name                   = models.CharField(max_length=30)
    description            = models.CharField(max_length=200)
    picture                = models.ImageField(null=True, blank = True, upload_to="images/")
    number_of_reservations = models.IntegerField()
    price_staff            = models.DecimalField(max_digits=5, decimal_places=2)
    price_student          = models.DecimalField(max_digits=5, decimal_places=2)

class Reservation(models.Model):
    order_no    = models.BigAutoField(primary_key = True)
    datetime    = models.DateTimeField(auto_now_add=True)
    meal        = models.ForeignKey(Meal, on_delete=models.CASCADE)
    collected   = models.BooleanField(default=False)
    