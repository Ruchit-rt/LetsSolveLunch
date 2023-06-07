from django.contrib import admin

from .models import Meal, Reservation, Restaurant

admin.site.register(Restaurant)
admin.site.register(Meal)
admin.site.register(Reservation)