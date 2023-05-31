from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

def say_hello(request):
    return render(request, 'hello.html')
            
