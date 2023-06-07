from django.contrib import admin

from .models import Customer, Meal, Reservation

admin.site.register(Meal)
admin.site.register(Reservation)
admin.site.register(Customer)