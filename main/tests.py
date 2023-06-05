from django.test import TestCase
from main.models import Meal
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO
from django.http import QueryDict
from consumer.views import reserve_success_view

# Create your tests here.
class MealCreationTestCase(TestCase):
    def setUp(self):
        Meal.objects.create(name = "Choc Croissant Brunch",
        description = "Chocolate Ganche sprinkle croissant with black americano",
        picture = "croissantCoffee.jpg",
        number_of_reservations = 3,
        price_staff = 4.99,
        price_student = 3.99
        )

    def test_meal_is_added_to_menu(self):
        """Meals are created"""
        meal : Meal = Meal.objects.get(name="Choc Croissant Brunch")
        self.assertEqual(meal.description, "Chocolate Ganche sprinkle croissant with black americano")

class MealReservationTestCase(MealCreationTestCase):
    def test_reserve_button_press_increases_count(self):
        """Make a meal"""
        meal : Meal = Meal.objects.get(name="Choc Croissant Brunch")
        old_count = meal.number_of_reservations

        request = WSGIRequest({
        'REQUEST_METHOD': 'POST',
        'wsgi.input': StringIO(),
        })

        request.POST = QueryDict('', mutable=True)
        request.POST['meal_id'] = str(meal.meal_id)

        """reserve a meal"""
        reserve_success_view(request)

        self.assertEqual(Meal.objects.get(name="Choc Croissant Brunch").number_of_reservations, (old_count + 1))
