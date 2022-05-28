from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.defaults import server_error

import json
import io, base64
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import os
import dotenv
from decouple import Config, RepositoryEnv
from pathlib import Path

from .models import BenchmarkResult

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DOTENV_FILE = BASE_DIR / '../.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

REDEEM_SECRET = env_config.get('REDEEM_SECRET')


def line_graph(points):
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

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64


def multi_graph(points):
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

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64


def bar_graph(points):
    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1,1,1)
    x_vals = []
    y_vals = []

    for d in points:
        x_vals.append(d["label"])
        y_vals.append(d["y"])

    ax.bar(x_vals, y_vals)
    ax.set(xlabel='', ylabel='time')

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64


def histogramm(points):
    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1,1,1)
    x_vals = []
    y_vals = []

    ax.hist(points, bins=np.arange(min(points), max(points) + 1, 1))
    ax.set(xlabel='time', ylabel='')
    ax.grid(axis='x', color='red', alpha=0.2)

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64


@require_http_methods(["POST"])
def upload(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    model = body.get('model', '')
    user_agent = body.get('user_agent', '')
    workerid = body.get('workerid', '')
    benchmark_results = body.get('benchmark_results', [])
    times = body.get('times', [])
    
    try:
        assert len(benchmark_results) == 13
        b64_charts = []
        # b64_charts.append(line_graph(benchmark_results[0]))
        # b64_charts.append(bar_graph(benchmark_results[1]))
        # b64_charts.append(line_graph(benchmark_results[2]))
        # b64_charts.append(line_graph(benchmark_results[3]))
        # b64_charts.append(line_graph(benchmark_results[4]))
        # b64_charts.append(line_graph(benchmark_results[5]))
        # b64_charts.append(line_graph(benchmark_results[6]))
        # b64_charts.append(line_graph(benchmark_results[7]))
        # b64_charts.append(histogramm(benchmark_results[8]))
        # b64_charts.append(line_graph(benchmark_results[9]))
        # b64_charts.append(line_graph(benchmark_results[10]))
        # b64_charts.append(multi_graph(benchmark_results[11]))
        # b64_charts.append(line_graph(benchmark_results[12]))

        b = BenchmarkResult(model=model, user_agent=user_agent, benchmark_results=benchmark_results, b64_charts=b64_charts, times=times)
        b.save()
        code = hashlib.shake_128(bytes(workerid + REDEEM_SECRET, encoding='utf-8')).hexdigest(12)
        return HttpResponse(code, status=200)
    except:
        return server_error(request)
