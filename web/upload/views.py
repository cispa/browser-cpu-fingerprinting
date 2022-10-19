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
classifiers['L3Presence'] = load(
    BASE_DIR / '../classification/.cache/classifiers/L3Presence.dump')
classifiers['L1Associativities'] = load(
    BASE_DIR / '../classification/.cache/classifiers/L1Associativities.dump')
classifiers['AMDvsIntel'] = load(
    BASE_DIR / '../classification/.cache/classifiers/AMDvsIntel.dump')
classifiers['Microarchitectures'] = load(
    BASE_DIR / '../classification/.cache/classifiers/Microarchitectures.dump')
classifiers['Microarchitecturesgroupedbydesign'] = load(
    BASE_DIR / '../classification/.cache/classifiers/Microarchitecturesgroupedbydesign.dump')
classifiers['NumberofThreads'] = load(
    BASE_DIR / '../classification/.cache/classifiers/NumberofThreads.dump')
classifiers['Modelswithexecutiontimes'] = load(
    BASE_DIR / '../classification/.cache/classifiers/Modelswithexecutiontimes.dump')


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


def prepare_l2(cachesize_benchmark_small, cachesize_benchmark_large):
    tmp = []
    for d in cachesize_benchmark_small:
        tmp += [d['y']]
    for d in cachesize_benchmark_large:
        tmp += [d['y']]
    return tmp


def prepare_l3(cachesize_benchmark_small, cachesize_benchmark_large):
    tmp = []
    for d in cachesize_benchmark_small:
        tmp += [d['y']]
    for d in cachesize_benchmark_large:
        tmp += [d['y']]
    return tmp


def prepare_l1asso(cacheasso_benchmark):
    tmp = []
    for d in cacheasso_benchmark:
        tmp += [d['y']]
    return tmp


def prepare_cores(cores):
    tmp = []
    for d in cores[:17]:
        tmp += [d['y']]
    return tmp


def prepare_uarch(cachesize_benchmark_small, cachesize_benchmark_large, cacheasso_benchmark, tlb_benchmark, cores):
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


def prepare_amd_vs_intel(cachesize_benchmark_small, cachesize_benchmark_large, tlb_benchmark):
    tmp = []
    for d in cachesize_benchmark_small[3::2]:
        tmp += [d['y']]
    for d in cachesize_benchmark_large:
        tmp += [d['y']]
    for d in tlb_benchmark[::2]:
        tmp += [d['y']]
    return tmp


@require_http_methods(["POST"])
def upload(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    benchmark_results = body.get('benchmark_results', [])
    times = body.get('times', [])

    try:
        assert len(benchmark_results) == 5
        assert len(times) == 5
        cacheasso_benchmark = benchmark_results[0]
        cachesize_benchmark_small = benchmark_results[1]
        cachesize_benchmark_large = benchmark_results[2]
        tlb_benchmark = benchmark_results[3]
        cores = benchmark_results[4]

        M1vsRest_data = prepare_M1vsRest(
            cacheasso_benchmark, cachesize_benchmark_small, cachesize_benchmark_large, tlb_benchmark, cores)
        l1_data = prepare_l1(cachesize_benchmark_small)
        l2_data = prepare_l2(cachesize_benchmark_small,
                             cachesize_benchmark_large)
        l3_data = prepare_l3(cachesize_benchmark_small,
                             cachesize_benchmark_large)
        l1asso_data = prepare_l1asso(cacheasso_benchmark)
        cores_data = prepare_cores(cores)
        uarch_data = prepare_uarch(
            cachesize_benchmark_small, cachesize_benchmark_large, cacheasso_benchmark, tlb_benchmark, cores)
        vendor_data = prepare_amd_vs_intel(
            cachesize_benchmark_small, cachesize_benchmark_large, tlb_benchmark)

        # i am deeply sorry
        predictions = dict()
        predictions['M1vsRest'] = list(
            classifiers['M1vsRest'].predict([M1vsRest_data]))[0]
        predictions['M1vsRestproba'] = list(
            classifiers['M1vsRest'].predict_proba([M1vsRest_data]))[0][list(classifiers['M1vsRest'].classes_).index(predictions['M1vsRest'])]
        predictions['L1CacheSizes'] = int(list(
            classifiers['L1CacheSizes'].predict([l1_data]))[0])
        predictions['L1CacheSizesproba'] = list(
            classifiers['L1CacheSizes'].predict_proba([l1_data]))[0][list(classifiers['L1CacheSizes'].classes_).index(predictions['L1CacheSizes'])]
        predictions['L2CacheSizes'] = int(list(
            classifiers['L2CacheSizes'].predict([l2_data]))[0])
        predictions['L2CacheSizesproba'] = list(
            classifiers['L2CacheSizes'].predict_proba([l2_data]))[0][list(classifiers['L2CacheSizes'].classes_).index(predictions['L2CacheSizes'])]
        predictions['L3CacheSizes'] = int(list(
            classifiers['L3CacheSizes'].predict([l3_data]))[0])
        predictions['L3CacheSizesproba'] = list(
            classifiers['L3CacheSizes'].predict_proba([l3_data]))[0][list(classifiers['L3CacheSizes'].classes_).index(predictions['L3CacheSizes'])]
        predictions['L3Presence'] = int(list(
            classifiers['L3Presence'].predict([l3_data]))[0])
        predictions['L3Presenceproba'] = list(
            classifiers['L3Presence'].predict_proba([l3_data]))[0][list(classifiers['L3Presence'].classes_).index(predictions['L3Presence'])]
        predictions['L1Associativities'] = int(list(
            classifiers['L1Associativities'].predict([l1asso_data]))[0])
        predictions['L1Associativitiesproba'] = list(
            classifiers['L1Associativities'].predict_proba([l1asso_data]))[0][list(classifiers['L1Associativities'].classes_).index(predictions['L1Associativities'])]
        predictions['AMDvsIntel'] = list(
            classifiers['AMDvsIntel'].predict([vendor_data]))[0]
        predictions['AMDvsIntelproba'] = list(
            classifiers['AMDvsIntel'].predict_proba([vendor_data]))[0][list(classifiers['AMDvsIntel'].classes_).index(predictions['AMDvsIntel'])]
        predictions['Microarchitectures'] = list(
            classifiers['Microarchitectures'].predict([uarch_data]))[0]
        predictions['Microarchitecturesproba'] = list(
            classifiers['Microarchitectures'].predict_proba([uarch_data]))[0][list(classifiers['Microarchitectures'].classes_).index(predictions['Microarchitectures'])]
        predictions['Microarchitecturesgroupedbydesign'] = list(
            classifiers['Microarchitecturesgroupedbydesign'].predict([uarch_data]))[0]
        predictions['Microarchitecturesgroupedbydesignproba'] = list(
            classifiers['Microarchitecturesgroupedbydesign'].predict_proba([uarch_data]))[0][list(classifiers['Microarchitecturesgroupedbydesign'].classes_).index(predictions['Microarchitecturesgroupedbydesign'])]
        predictions['NumberofThreads'] = int(list(
            classifiers['NumberofThreads'].predict([cores_data]))[0])
        predictions['NumberofThreadsproba'] = list(
            classifiers['NumberofThreads'].predict_proba([cores_data]))[0][list(classifiers['NumberofThreads'].classes_).index(predictions['NumberofThreads'])]
        predictions['Modelswithexecutiontimes'] = list(
            classifiers['Modelswithexecutiontimes'].predict([times]))[0]
        predictions['Modelswithexecutiontimesproba'] = list(
            classifiers['Modelswithexecutiontimes'].predict_proba([times]))[0][list(classifiers['Modelswithexecutiontimes'].classes_).index(predictions['Modelswithexecutiontimes'])]

        return HttpResponse(json.dumps(predictions), status=200)
    except Exception as ex:
        print(ex)
        return server_error(request)
