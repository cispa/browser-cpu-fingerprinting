from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json
import matplotlib
import base64
import matplotlib.pyplot as plt
import numpy as np


@require_http_methods(["POST"])
def line(request):
    response = HttpResponse()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    points = body.get('points', list())

    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1,1,1)
    x_vals = []
    y_vals = []

    for d in points:
        x_vals.append(d["x"])
        y_vals.append(d["y"])

    ax.plot(x_vals, y_vals)
    ax.grid(axis='x', color='0.95')
    ax.set(xlabel='', ylabel='time')

    fig.savefig(response)
    return response


@require_http_methods(["POST"])
def hist(request):
    response = HttpResponse()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    points = body.get('points', list())

    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1,1,1)
    x_vals = []
    y_vals = []

    # ax.set_ylim(0, 1000)
    # ax.hist(points, range=(0, 300), bins=300)
    ax.hist(points, bins=np.arange(min(points), max(points) + 1, 1))
    ax.set(xlabel='time', ylabel='')
    ax.grid(axis='x', color='red', alpha=0.2)

    fig.savefig(response)
    return response


@require_http_methods(["POST"])
def multiline(request):
    response = HttpResponse()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    points = body.get('points', list())

    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1,1,1)

    for line in points:
        x_vals = []
        y_vals = []
            
        for d in line:
            x_vals.append(d["x"])
            y_vals.append(d["y"])

        ax.plot(x_vals, y_vals)

    ax.grid(axis='x', color='0.95')
    ax.set(xlabel='', ylabel='time')

    fig.savefig(response)
    return response


@require_http_methods(["POST"])
def bar(request):
    response = HttpResponse()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    points = body.get('points', list())

    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1,1,1)
    x_vals = []
    y_vals = []

    for d in points:
        x_vals.append(d["label"])
        y_vals.append(d["y"])

    ax.bar(x_vals, y_vals)
    ax.set(xlabel='', ylabel='time')

    fig.savefig(response)
    return response