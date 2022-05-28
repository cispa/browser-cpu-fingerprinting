from django.contrib import messages
#from django.core.checks import messages
from django.shortcuts import render
from django.shortcuts import reverse, redirect
from django.http import HttpResponse


def cacheSize(request):
    return render(request, 'cache/size.html')


def cacheAssociativity(request):
    return render(request, 'cache/associativity.html')


def tlbSize(request):
    return render(request, 'tlb/size.html')


def miscCores(request):
    return render(request, 'misc/cores.html')


def miscBits(request):
    return render(request, 'misc/bits.html')


def miscPagesize(request):
    return render(request, 'misc/pagesize.html')


def miscPrefetcher(request):
    return render(request, 'misc/prefetcher.html')


def performanceSingle(request):
    return render(request, 'performance/single.html')


def performanceMulti(request):
    return render(request, 'performance/multi.html')


def performanceMemory(request):
    return render(request, 'performance/memory.html')


def bufferLoad(request):
    return render(request, 'buffer/load.html')


def bufferStore(request):
    return render(request, 'buffer/store.html')


def timerPrecision(request):
    return render(request, 'misc/timer.html')