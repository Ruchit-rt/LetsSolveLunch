from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/media/', views.media_view),
    path('home/reserve/', views.reserve_view),
     path('home/', views.home_view, name='home'),
]