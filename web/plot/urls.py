from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('line/', views.line, name='line'),
    path('bar/', views.bar, name='bar'),
    path('multiline/', views.multiline, name='multiline'),
    path('hist/', views.hist, name='hist'),
]