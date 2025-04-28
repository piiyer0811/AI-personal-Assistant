from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You are at your personal assistant")

def indextwo(request):
    return HttpResponse("Hello, world. You are at your personal assistant 2")


