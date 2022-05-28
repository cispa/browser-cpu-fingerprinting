from django.contrib import messages
#from django.core.checks import messages
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse


def landing(request):
    return render(request, 'landing.html')


def start(request):
    return render(request, 'home.html')


def problem(request):
    return render(request, 'problem.html')


def overview(request):
    return render(request, 'overview.html')