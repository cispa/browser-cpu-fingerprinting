from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('start/', views.start, name='start'),
    path('overview/', views.overview, name='overview'),
    path('problem/', views.problem, name='problem'),
]