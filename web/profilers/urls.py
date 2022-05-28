from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('cache/size', views.cacheSize, name='cacheSize'),
    path('cache/associativity', views.cacheAssociativity, name='cacheAssociativity'),
    path('tlb/size', views.tlbSize, name='tlbSize'),
    path('misc/cores', views.miscCores, name='miscCores'),
    path('misc/bits', views.miscBits, name='miscBits'),
    path('misc/pagesize', views.miscPagesize, name='miscPagesize'),
    path('misc/prefetcher', views.miscPrefetcher, name='miscPrefetcher'),
    path('timer/', views.timerPrecision, name='timerPrecision'),
    path('performance/single', views.performanceSingle, name='performanceSingle'),
    path('performance/multi', views.performanceMulti, name='performanceMulti'),
    path('performance/memory', views.performanceMemory, name='performanceMemory'),
    path('buffer/load', views.bufferLoad, name='bufferLoad'),
    path('buffer/store', views.bufferStore, name='bufferStore'),
]