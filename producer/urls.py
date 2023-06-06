from django.urls import path
from . import views

urlpatterns = [
    path('mycafe/', views.mycafe_view, name='mycafe'),
    path('menu/', views.add_menu_view, name='menu'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout_result/', views.checkout_result_view, name='checkout'),
]