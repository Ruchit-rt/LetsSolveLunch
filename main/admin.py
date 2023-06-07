from django.contrib import admin

from .models import Meal, Reservation, Restaurant, Customer

admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(Reservation)
admin.site.register(Customer)