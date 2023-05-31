from django.urls import path
from . import views

urlpatterns = [
    path('mycafe/', views.mycafe_view, name='mycafe')
]