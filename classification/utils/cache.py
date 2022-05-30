import sqlite3
import json
import csv
import pgdumplib
import time
from pathlib import Path
import pickle
import os


def model_filter(db_models):
    # large filter because of people not following the standard procedure
    db_models = list(map(lambda x: x.replace('  ', ' '), db_models))
    db_models = list(map(lambda x: x.replace('  ', ' '), db_models))
    db_models = list(map(lambda x: x.replace('  ', ' '), db_models))
    db_models = list(map(lambda x: x.replace('  ', ' '), db_models))
    db_models = list(map(lambda x: x.replace('  ', ' '), db_models))
    db_models = list(map(lambda x: x.replace(' - ', '-'), db_models))
    db_models = list(map(lambda x: x.split(' CPU')[0] if 'Pentium' not in x and 'Xeon' not in x and 'Celeron' not in x and 'Duo' not in x else x, db_models))
    db_models = list(map(lambda x: x.split(' cpu')[0] if 'Pentium' not in x and 'Xeon' not in x and 'Celeron' not in x and 'Duo' not in x else x, db_models))
    db_models = list(map(lambda x: x.split(' w/')[0], db_models))
    db_models = list(map(lambda x: x.replace('(IM)', '(TM)'), db_models))
    db_models = list(map(lambda x: x.replace('(tm)', '(TM)'), db_models))
    db_models = list(map(lambda x: x.replace('(r)', '(R)'), db_models))
    db_models = list(map(lambda x: x.replace('Intel (R)', 'Intel(R)'), db_models))
    db_models = list(map(lambda x: x.replace('Core (TM)', 'Core(TM)'), db_models))
    db_models = list(map(lambda x: x.replace('Itel', 'Intel'), db_models))
    db_models = list(map(lambda x: x.replace('Amd', 'AMD'), db_models))
    db_models = list(map(lambda x: x.replace('3700x', '3700X'), db_models))
    db_models = list(map(lambda x: x.replace('3250u', '3250U'), db_models))
    db_models = list(map(lambda x: x.replace('RYZEN', 'Ryzen'), db_models))
    db_models = list(map(lambda x: x.replace('Processor\\t', ''), db_models))
    db_models = list(map(lambda x: x.replace('2700k', '2700K'), db_models))
    db_models = list(map(lambda x: x.replace('4790k', '4790K'), db_models))
    db_models = list(map(lambda x: x.replace('6700k', '6700K'), db_models))
    db_models = list(map(lambda x: x.replace('3770k', '3770K'), db_models))
    db_models = list(map(lambda x: x.replace('i7-11657', 'i7-1165G7'), db_models))
    db_models = list(map(lambda x: 'AMD Athlon 64 X2 5000B' if x == 'AMD Athlon(tm) Dual Core Processor 5000B' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i9-9900K' if x == '9900K' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(tm) i5-5200U' if x == 'intel (R) core (tm) i5-5200U 2.20ghz' else x, db_models))
    db_models = list(map(lambda x: 'AMD A9-9425' if x == 'AMD A9-9425 Radeon R5, Compute Cores 2C+3G' else x, db_models))
    db_models = list(map(lambda x: 'Kirin 960' if x == 'Hisilicon Kirin 960 (Huawei P10 VTR-L09)' else x, db_models))
    db_models = list(map(lambda x: 'AMD Turion(TM) X2 Ultra Dual-Core ZM-87' if x == 'AMD Turion(tm) X2 Ultra Dual-Core Mobile ZM-87' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i3-8130U' if x == 'Intel Core i3-8130U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-5287U' if x == 'intel core i5-5287U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8300H' if x == 'i5-8300H' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i3-6100' if x == 'i3-6100' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 7 4800H' if x == 'AMD Ryzen 4800H' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8250U' if x == 'Intel core i5-8250u' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-4700' if x == 'Intel Core i7-4700' else x, db_models))
    db_models = list(map(lambda x: 'AMD FX(tm)-8320E' if x == 'AMD FX 8320E' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-2520M' if x == 'Intel(R) Core(TM) 15-2520M' else x, db_models))
    db_models = list(map(lambda x: 'AMD A10-9600P' if x == 'AMD A10-9600P RADEON R5, 10 COMPUTE CORES 4C+6G' else x, db_models))
    db_models = list(map(lambda x: 'AMD Athlon(TM) X4 860K' if x == 'AMD Athlon(TM) X4 860K Quad Core Processor' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 5 2600X' if x == 'AMD Ryzen 5 2600x 6 core processor' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-7500U' if x == 'Intel(R) core (TM) i7-7500U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-3570' if x == 'i5-3570' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Celeron(R) N4000' if x == 'celeron n4000' else x, db_models))
    db_models = list(map(lambda x: 'AMD Athlon 64 X2 5000B' if x == 'AMD Athlon(TM) Dual Core Processor 5000B' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-5200U' if x == 'intel (R) core (TM) i5-5200U 2.20ghz' else x, db_models))
    db_models = list(map(lambda x: 'AMD Turion(TM) X2 Ultra Dual-Core ZM-87' if x == 'AMD Turion(TM) X2 Ultra Dual-Core Mobile ZM-87' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-7700HQ' if x == 'Intel i7-7700HQ' else x, db_models))
    db_models = list(map(lambda x: x.split(' @')[0], db_models))
    db_models = list(map(lambda x: x.split('11th Gen ')[1] if len(x.split('11th Gen ')) > 1 else x, db_models))
    db_models = list(map(lambda x: x.split(' with')[0], db_models))
    db_models = list(map(lambda x: x.split(' Quad-Core')[0], db_models))
    db_models = list(map(lambda x: x.split(' Six-Core')[0], db_models))
    db_models = list(map(lambda x: x.split(' Eight-Core')[0], db_models))
    db_models = list(map(lambda x: x.split(' quad-core')[0], db_models))
    db_models = list(map(lambda x: x.split(' six-core')[0], db_models))
    db_models = list(map(lambda x: x.split(' eight-core')[0], db_models))
    db_models = list(map(lambda x: x.split(' 6-Core')[0], db_models))
    db_models = list(map(lambda x: x.split(' 8-Core')[0], db_models))
    db_models = list(map(lambda x: x.split(' 12-Core')[0], db_models))
    db_models = list(map(lambda x: x.split(' 6-core')[0], db_models))
    db_models = list(map(lambda x: x.split(' 8-core')[0], db_models))
    db_models = list(map(lambda x: x.split(' 12-core')[0], db_models))
    db_models = list(map(lambda x: x.split('machdep.cpu.brand_string: ')[1] if len(x.split('machdep.cpu.brand_string: ')) > 1 else x, db_models))
    db_models = list(map(lambda x: 'AMD ' + x if x.startswith('Ryzen') else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) ' + x if x.startswith('Pentium') else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) ' + x if x.startswith('Core') else x, db_models))
    db_models = list(map(lambda x: 'Apple M1' if 'Apple M1' in x else x, db_models))
    db_models = list(map(lambda x: x.strip(), db_models))
    db_models = list(map(lambda x: 'AMD FX(TM)-8320E' if x == 'AMD FX 8320E' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8265U' if x == 'Intel(R) Core(TM) i5-8265UCPU' else x, db_models))
    db_models = list(map(lambda x: 'AMD FX(TM)-6300' if x == 'AMD FX 6300' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 5 3500U' if x == 'AMD Ryzen5 3500U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-1035G4' if x == 'i5-1035G4' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-8550U' if x == 'i7-855OU' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 9 3900X' if x == 'AMD Ryzen 3900x' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-2400' if x == 'Intel(R) Core(TM) i-5 2400' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-6500' if x == 'Intel Core i5-6500' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Celeron(R) N4000' if x == 'Intel(R) Celeron(R) N4000 CPU' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-4790K' if x == 'Intel Core-i7-4790K' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 3 3250U' if x == 'AMD Ryzen 3 325OU' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-3470' if x == 'i5-3470' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-6500' if x == 'i5 6500' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-10210U' if x == 'Intel(R) Core(TM) i5-1021OU' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 7 2700X' if x == 'amd ryzen 7 2700x' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-9300H' if x == 'i5-9300H' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-7500' if x == 'i5 7500' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-4690K' if x == 'i5 4690k' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-5820K' if x == 'i7-5820k' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-6500' if x == 'i5-6500' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-4210U' if x == 'i5-4210U' else x, db_models))
    db_models = list(map(lambda x: 'AMD FX-7500' if x == 'AMD FX-7500 Radeon R7, 10 Compute Cores 4C+6G' else x, db_models))
    db_models = list(map(lambda x: 'AMD A9-9425' if x == 'AMD A9-9425 RADEON R5, 5 COMPUTE CORES 2C+3G 3.10 GHz' else x, db_models))
    db_models = list(map(lambda x: 'AMD A12-9720P' if x == 'AMD A12-9720P RADEON R7, 12 COMPUTE CORES 4C+8G' else x, db_models))
    db_models = list(map(lambda x: 'AMD A9-9420' if x == 'AMD A9-9420 RADEON R5, 5 COMPUTE CORES 2C+3G' else x, db_models))
    db_models = list(map(lambda x: 'AMD Phenom II X4 925' if x == 'AMD Phenom II X4 925 processor' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-5300U' if x == 'Name Intel(R) Core(TM) i5-5300U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8265U' if x == 'Intel(R) Core(TM) i58265U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i3-4030U' if x == 'Intel(R) Core TM I3-403OU' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-3470' if x == 'Intel Core i5-3470' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-10750H' if x == 'Intel Core i7-10750H' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-4770K' if x == 'Intel(R) Core(TM) i7-4770k' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-8700' if x == 'intel(R) core (TM) i7-8700' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-7300HQ' if x == 'i5-7300HQ' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i3-5020U' if x == 'Intel( R ) Core ( TM ) i3-502ou' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-4210U' if x == 'Intel(R) core(TM) i5-4210U' else x, db_models))
    db_models = list(map(lambda x: 'AMD A8-4500M APU' if x == 'AMD A8 -4500M APU' else x, db_models))
    db_models = list(map(lambda x: 'AMD FX(TM)-8350' if x == 'AMD FX-8350' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-9750H' if x == 'Intel(R) Core(TM) i7- 9750HCPU' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 9 3900X' if x == 'AMD Ryzen 9 3900x' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-6700' if x == 'intel core i7-6700' else x, db_models))
    db_models = list(map(lambda x: 'AMD A10-9620P' if x == 'AMD A10-9620P RADEON R5, 10 COMPUTE CORES 4C+6G' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-4670K' if x == 'Intel Core i5 4670K' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-870' if x == 'Intel(R) Core(TM) i7 870' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-8565U' if x == 'Intel(R) Core TM i7-8565U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8400' if x == ': Intel(R) Core(TM) i5-8400' else x, db_models))
    db_models = list(map(lambda x: 'AMD FX(TM)-8350' if x == 'AMD FX<tm>-8350' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 7 3700X' if x == 'AMD Ryzen 3700X' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8400' if x == 'Intel(R) Core(TM) i5- 8400' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-8400' if x == 'Inter(R) Core(TM) i5-8400' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-5200U' if x == 'Intel(R) Core(TM) i5-5200u' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-7200U' if x == 'i5-7200U' else x, db_models))
    db_models = list(map(lambda x: 'AMD Ryzen 7 1700' if x == 'AMD Ryzen 1700' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-5287U' if x == 'Intel(R)Core(TM) i5-5287U' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-3320M' if x == 'intel core i5- 3320m' else x, db_models))
    db_models = list(map(lambda x: 'AMD A10-8700P' if x == 'AMD A10-8700P Radeon R6, 10 Compute Cores 4C+6G' else x, db_models))
    db_models = list(map(lambda x: 'AMD Turion(TM) II P520' if x == 'AMD Turion(TM) II P520 Dual-Core Processor' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i5-7300HQ' if x == 'Intel Core I5-7300HQcpu' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Core(TM) i7-7700HQ' if x == 'Intel(R) Core(I) I7-7700HQ' else x, db_models))
    db_models = list(map(lambda x: 'Intel(R) Pentium(R) CPU N3710' if x == 'intel pentium N3710' else x, db_models))
    db_models = list(map(lambda x: 'AMD Athlon(TM) Silver 3050U' if x == 'AMD athlon silver 3050U' else x, db_models))
    return db_models


def load_database():
    cache_path = Path(".cache")
    if cache_path.exists():
        with open(cache_path / "benchmarks.pkl", 'rb') as f:
            benchmarks = pickle.load(f)
        with open(cache_path / "db_models.pkl", 'rb') as f:
            db_models = pickle.load(f)
        return db_models, benchmarks

    print('[-]  Loading from sqlite3 database')
    eliminated = 0
    start_time = time.time()
    con = sqlite3.connect('/path/to/db.sqlite3')

    db_models = []
    # pagesize_benchmarks = []
    # prefetcher_benchmarks = []
    cacheasso_benchmarks = []
    cachesize_benchmarks_small = []
    cachesize_benchmarks_large = []
    tlb_benchmarks = []
    # timer_time = []
    timer_diff = []
    # memory_latencies = []
    # loadbuffer_benchmarks = []
    singleperf_benchmarks = []
    # multiperf_benchmarks = []
    cores = []
    execution_times = []

    cursor = con.execute("SELECT * FROM upload_benchmarkresult;")
    for row in cursor.fetchall():
        # exclude my own CPU from the dataset
        if row[1] == 'Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz':
            eliminated += 1
            continue
        db_models += [row[1]]
        # during the first iteration we did not collect execution times
        execution_times += [[]]
        benchmarks = json.loads(row[3])
        # pagesize_benchmarks += [benchmarks[0]]
        # prefetcher_benchmarks += [benchmarks[1]]
        cacheasso_benchmarks += [benchmarks[2]]
        cachesize_benchmarks_small += [benchmarks[3]]
        cachesize_benchmarks_large += [benchmarks[4]]
        tlb_benchmarks += [benchmarks[5]]
        # timer_time += [benchmarks[6]]
        timer_diff += [benchmarks[7][:4]]
        # memory_latencies += [benchmarks[8]]
        # loadbuffer_benchmarks += [benchmarks[9]]
        singleperf_benchmarks += [benchmarks[10]]
        # multiperf_benchmarks += [benchmarks[11]]
        cores += [benchmarks[12]]

    print('[-]  Loading from PostgreSQL database')
    dump = pgdumplib.load('/path/to/db.dump')
    for row in dump.table_data('public', 'upload_benchmarkresult'):
        db_models += [row[1]]
        execution_times += [json.loads(row[5])]
        benchmarks = json.loads(row[3])
        # pagesize_benchmarks += [benchmarks[0]]
        # prefetcher_benchmarks += [benchmarks[1]]
        cacheasso_benchmarks += [benchmarks[2]]
        cachesize_benchmarks_small += [benchmarks[3]]
        cachesize_benchmarks_large += [benchmarks[4]]
        tlb_benchmarks += [benchmarks[5]]
        # timer_time += [benchmarks[6]]
        timer_diff += [benchmarks[7][:4]]
        # memory_latencies += [benchmarks[8]]
        # loadbuffer_benchmarks += [benchmarks[9]]
        singleperf_benchmarks += [benchmarks[10]]
        # multiperf_benchmarks += [benchmarks[11]]
        cores += [benchmarks[12]]

    benchmarks = dict()
    benchmarks['cacheasso_benchmarks'] = cacheasso_benchmarks
    benchmarks['cachesize_benchmarks_small'] = cachesize_benchmarks_small
    benchmarks['cachesize_benchmarks_large'] = cachesize_benchmarks_large
    benchmarks['tlb_benchmarks'] = tlb_benchmarks
    # benchmarks['loadbuffer_benchmarks'] = loadbuffer_benchmarks
    benchmarks['singleperf_benchmarks'] = singleperf_benchmarks
    # benchmarks['multiperf_benchmarks'] = multiperf_benchmarks
    benchmarks['cores'] = cores
    benchmarks['execution_times'] = execution_times
    benchmarks['timer'] = timer_diff
    # benchmarks['memory_latencies'] = memory_latencies

    db_models = model_filter(db_models)

    print('[-]  Loaded data from databases in %s seconds' % (time.time() - start_time))
    print('[-]  Eliminated %s Entries' % (eliminated))

    if not cache_path.exists():
        os.mkdir(cache_path)

    print('[-]  Starting Pickle')
    with open(cache_path / "benchmarks.pkl", 'wb') as f:
        pickle.dump(benchmarks, f)
    with open(cache_path / "db_models.pkl", 'wb') as f:
        pickle.dump(db_models, f)
    print('[-]  Pickle done')

    return db_models, benchmarks


def load_csv():
    print('[-]  Loading target data from CSV')
    res = {
        'name': [],
        'rname': [],
        'l1': [],
        'l2': [],
        'l3': [],
        'l1asso': [],
        'smt': [],
        'threads': [],
        'base': [],
        'boost': [],
        'uarch': [],
        'tlb': []
    }

    with open('../data/cpus.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            res['name'] += [row['name']]
            res['rname'] += [row['rname']]
            res['l1'] += [int(row['l1'])]
            res['l2'] += [int(row['l2'])]
            res['l3'] += [int(row['l3']) if row['l3'] != '' else 0]
            res['l1asso'] += [int(row['l1asso']) if row['l1asso'] != '' else 0]
            res['smt'] += [int(row['cores']) != int(row['threads'])]
            res['threads'] += [int(row['threads']) if row['name'] != 'Apple M1' else 4]
            res['base'] += [int(100 * float(row['base']))]
            res['boost'] += [int(100 * float(row['boost']))]
            res['uarch'] += [row['microarchitecture']]
            res['tlb'] += [row['l1dtlb']]
    print('[-]  Done loading target data from CSV')
    return res