from django.urls import path
from . import views

urlpatterns = [
    path('mycafe/', views.mycafe_view, name='mycafe'),
    path('displaymenu/', views.menu_view, name='displaymenu'),
    path('addmenu/', views.add_menu_view, name='addmenu'),
    path('edit_menu/', views.edit_menu_view, name='editmenu'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout_result/', views.checkout_result_view, name='checkout'),
]