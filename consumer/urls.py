from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/media/', views.media_view),
    path('home/reserve_success/emailsent/', views.emailsent_view),
    path('home/reserve_success/', views.reserve_success_view),
    path('home/', views.home_view, name='home'),
    path('home/confirm_reserve/', views.confirm_reserve_view),
]