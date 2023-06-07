from django.test import TestCase
from main.models import Meal, Customer
from django.test import RequestFactory
from consumer.views import reserve_success_view

# Create your tests here.
class MealCreationTestCase(TestCase):
    def setUp(self):
        Meal.objects.create(name = "Choc Croissant Brunch",
        description = "Chocolate Ganche sprinkle croissant with black americano",
        picture = "croissantCoffee.jpg",
        number_of_reservations = 3,
        price_staff = 4.99,
        price_student = 3.99)

        Customer.objects.create(name="Mark", email="a@b.com")

    def test_meal_is_added_to_menu(self):
        """Meals are created"""
        meal : Meal = Meal.objects.get(name="Choc Croissant Brunch")
        self.assertEqual(meal.description, "Chocolate Ganche sprinkle croissant with black americano")

class MealReservationTestCase(MealCreationTestCase):
    def test_reserve_button_press_increases_count(self):
        """Make a meal"""
        meal : Meal = Meal.objects.get(name="Choc Croissant Brunch")
        old_count = meal.number_of_reservations

        factory = RequestFactory()

        request = factory.post('/home/reserve_success/', {'meal_id': str(meal.meal_id)})
        request.session = {}
        request.session['user_email'] = "a@b.com"

        """reserve a meal"""
        reserve_success_view(request)

        self.assertEqual(Meal.objects.get(name="Choc Croissant Brunch").number_of_reservations, (old_count + 1))
