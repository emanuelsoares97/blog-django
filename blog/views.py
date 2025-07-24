from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Hello, world!</h1><p>Welcome to the blog homepage.</p>")

def about(request):
    return HttpResponse("<h1>About Us</h1><p>This is the about page of the blog.</p>")
