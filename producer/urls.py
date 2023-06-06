from django.urls import path
from . import views

urlpatterns = [
    path('mycafe/', views.mycafe_view, name='mycafe'),
    path('menu/', views.add_menu_view, name='menu')

]