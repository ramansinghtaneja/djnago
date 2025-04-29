from django.shortcuts import render
from django.http import JsonResponse
import json




def home(request):
    
    return render(request, 'api/home.html')

