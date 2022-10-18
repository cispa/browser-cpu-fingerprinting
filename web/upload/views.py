from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.defaults import server_error

import json
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import os
import dotenv
from decouple import Config, RepositoryEnv
from pathlib import Path
from joblib import load

from .models import BenchmarkResult

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DOTENV_FILE = BASE_DIR / '../.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))

classifiers = dict()
classifiers['M1vsRest'] = load(
    BASE_DIR / '../classification/.cache/classifiers/M1vsRest.dump')
classifiers['L1CacheSizes'] = load(
    BASE_DIR / '../classification/.cache/classifiers/L1CacheSizes.dump')
classifiers['L2CacheSizes'] = load(
    BASE_DIR / '../classification/.cache/classifiers/L2CacheSizes.dump')
classifiers['L3CacheSizes'] = load(
    BASE_DIR / '../classification/.cache/classifiers/L3CacheSizes.dump')
classifiers['L1Associativities'] = load(
    BASE_DIR / '../classification/.cache/classifiers/L1Associativities.dump')

def line_graph(points):
    fig = matplotlib.figure.Figure()
    ax = fig.add_subplot(1, 1, 1)
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
    ax = fig.add_subplot(1, 1, 1)

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
    ax = fig.add_subplot(1, 1, 1)
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
    ax = fig.add_subplot(1, 1, 1)
    x_vals = []
    y_vals = []

    ax.hist(points, bins=np.arange(min(points), max(points) + 1, 1))
    ax.set(xlabel='time', ylabel='')
    ax.grid(axis='x', color='red', alpha=0.2)

    flike = io.BytesIO()
    fig.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64


def prepare_M1vsRest(cacheasso_benchmark, cachesize_benchmark_small, cachesize_benchmark_large, tlb_benchmark, cores):
    tmp = []
    for d in cacheasso_benchmark[:17:2]:
        tmp += [d['y']]
    for d in cachesize_benchmark_small[3::2]:
        tmp += [d['y']]
    for d in cachesize_benchmark_large:
        tmp += [d['y']]
    for d in tlb_benchmark[::2]:
        tmp += [d['y']]
    for d in cores[:17]:
        tmp += [d['y']]
    return tmp


def prepare_l1(cachesize_benchmark_small):
    tmp = []
    for d in cachesize_benchmark_small[:int(len(cachesize_benchmark_small)/2)]:
        tmp += [d['y']]
    return tmp


@require_http_methods(["POST"])
def upload(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    benchmark_results = body.get('benchmark_results', [])
    times = body.get('times', [])

    try:
        # assert len(benchmark_results) == 5
        # assert len(times) == 5
        cacheasso_benchmark = benchmark_results[0]
        cachesize_benchmark_small = benchmark_results[1]
        cachesize_benchmark_large = benchmark_results[2]
        tlb_benchmark = benchmark_results[3]
        cores = benchmark_results[4]

        M1vsRest_data = prepare_M1vsRest(
            cacheasso_benchmark, cachesize_benchmark_small, cachesize_benchmark_large, tlb_benchmark, cores)
        l1_data = prepare_l1(cachesize_benchmark_small)

        predictions = dict()
        predictions['M1vsRest'] = list(
            classifiers['M1vsRest'].predict([M1vsRest_data]))[0]
        predictions['L1CacheSizes'] = int(list(
            classifiers['L1CacheSizes'].predict([l1_data]))[0])

        return HttpResponse(json.dumps(predictions), status=200)
    except Exception as ex:
        print(ex)
        return server_error(request)
