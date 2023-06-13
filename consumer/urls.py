from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/reserve_success/emailsent/', views.emailsent_view),
    path('home/reserve_success/', views.reserve_success_view),
    path('home/', views.home_view, name='home'),
    path('home/restaurant_menu', views.restaurant_menu_view, name='restaurant_menu'),
    path('home/confirm_reserve/', views.confirm_reserve_view),
    path('myaccount/', views.myaccount_view),
    path('order_history/', views.order_history_view),
    path('leaderboard/', views.leaderboard_view),
    path('departmentLeaderBoard/', views.departmentLeaderBoard_view),
    path('tag_filter/', views.tag_filter_view),
]