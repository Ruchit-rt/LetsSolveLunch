from django.shortcuts import render
from django.http import HttpResponse

def welcome_view(request):
    return render(request, 'welcome.html')

def reserveDynamic(request, slug):
    return render(request, 'reserveDynamic.html',{})
