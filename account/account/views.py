from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def make(request):
    return render(request, 'make.html')

def participate(request):
    return render(request, 'participate.html')
