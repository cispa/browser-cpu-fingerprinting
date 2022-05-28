import collections
from .uarch import replace_uarch_by_base

def prepare_l1(balance, db_models, cachesize_benchmarks_small, csv_models, csv_models_r, csv_l1):
    max_count = 30
    counts = {16 : max_count, 24 : max_count, 32 : max_count, 48 : max_count, 64 : 0, 128 : max_count}

    X_l1 = []
    y_l1 = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            j = csv_models.index(db_model)
        elif db_model in csv_models_r:     
            j = csv_models_r.index(db_model)
        else:
            continue
        
        p = csv_l1[j]
        if counts[p] < 1 and balance:
            continue
        counts[p] = counts[p] - 1

        tmp = []
        for d in cachesize_benchmarks_small[i][:int(len(cachesize_benchmarks_small[i])/2)]:
            tmp += [d['y']]

        X_l1 += [tmp]
        y_l1 += [p]

    return X_l1, y_l1


def prepare_l2(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, csv_models, csv_models_r, csv_l2):
    max_count = 26
    counts = {256 : max_count, 512 : max_count, 1024 : max_count, 1280 : 0, 2048 : max_count, 3072 : 0, 4096 : 0, 6042: 0, 12288 : max_count}

    X_l2 = []
    y_l2large = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            if len(cachesize_benchmarks_large[i]) > 1:  
                j = csv_models.index(db_model)

                p = csv_l2[j]
                if p in counts and counts[p] < 1 and balance:
                    continue
                if p in counts:
                    counts[p] = counts[p] - 1

                tmp = []
                for d in cachesize_benchmarks_small[i]:
                    tmp += [d['y']]
                for d in cachesize_benchmarks_large[i]:
                    tmp += [d['y']]
                X_l2 += [tmp]
                y_l2large += [p]

    return X_l2, y_l2large


def prepare_l3(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, csv_models, csv_models_r, csv_l3):
    max_count = 29
    counts = {0 : max_count, 2 : 0, 3 : max_count, 4 : max_count, 6 : max_count, 8 : max_count, 9 : max_count, 12 : max_count, 15 : 0, 16 : max_count, 20 : 0, 32 : max_count}

    X_l3 = []
    y_l3 = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            if len(cachesize_benchmarks_large[i]) > 1:  
                j = csv_models.index(db_model)

                p = csv_l3[j]
                if p in counts and counts[p] < 1 and balance:
                    continue
                if p in counts:
                    counts[p] = counts[p] - 1

                tmp = []
                for d in cachesize_benchmarks_small[i]:
                    tmp += [d['y']]
                for d in cachesize_benchmarks_large[i]:
                    tmp += [d['y']]
                X_l3 += [tmp]
                y_l3 += [p]

    return X_l3, y_l3


def prepare_l1asso(balance, db_models, cacheasso_benchmarks, csv_models, csv_models_r, csv_l1asso):
    max_count = 14
    counts = {2 : max_count, 4 : max_count, 6 : max_count, 8 : max_count, 12 : max_count}

    X_asso = []
    y_l1asso = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            j = csv_models.index(db_model)
            
            p = csv_l1asso[j]
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cacheasso_benchmarks[i]:
                tmp += [d['y']]
            X_asso += [tmp]
            y_l1asso += [p]

    return X_asso, y_l1asso


def prepare_frequency_base(balance, db_models, singleperf_benchmarks, multiperf_benchmarks, csv_models, csv_models_r, csv_base):
    max_count = 125
    counts = {0 : max_count, 1 : max_count, 2 : max_count, 3 : max_count, 4 : max_count}
    
    X_singleperf = []
    X_multiperf = []
    X_singleperf_boost = []
    X_combinedperf = []
    y_base = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            j = csv_models.index(db_model)
        elif db_model in csv_models_r:
            j = csv_models_r.index(db_model)
        else:
            continue
        
        p = 0
        # [150-199, 200-249, 250-299, 300-349, 350-399]
        if csv_base[j] <= 199:
            p = 0
        elif csv_base[j] <= 249:
            p = 1
        elif csv_base[j] <= 299:
            p = 2
        elif csv_base[j] <= 349:
            p = 3
        else:
            p = 4

        if p in counts and counts[p] < 1 and balance:
            continue
        if p in counts:
            counts[p] = counts[p] - 1

        tmp = []
        for d in singleperf_benchmarks[i]:
            tmp += [d['y']]
        X_singleperf += [tmp[:50] + tmp[500:550] + tmp[1000:1050]]
        X_singleperf_boost += [tmp[25:75] + tmp[525:575] + tmp[1025:1075]]
        
        tmp1 = []
        for core in multiperf_benchmarks[i]:
            for d in core:
                tmp1 += [d['y']]
        
        tmp2 = []
        for i in range(20):
            tmp2 += [tmp1[i * 5000]]
        X_multiperf += [tmp2]

        X_combinedperf += [tmp + tmp2]

        y_base += [p]

    return X_singleperf, X_multiperf, X_combinedperf, X_singleperf_boost, y_base


def prepare_frequency_boost(balance, db_models, singleperf_benchmarks, multiperf_benchmarks, csv_models, csv_models_r, csv_boost):
    max_count = 34
    counts = {0 : max_count, 1 : max_count, 2 : max_count, 3 : max_count, 4 : max_count, 5 : max_count}
    
    X_singleperf = []
    X_multiperf = []
    X_singleperf_boost = []
    X_combinedperf = []
    y_boost = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            j = csv_models.index(db_model)
        elif db_model in csv_models_r:
            j = csv_models_r.index(db_model)
        else:
            continue
             
        # [none, 300-349, 350-399, 400-449, 450-499, 500-549]
        if csv_boost[j] <= 299:
            p = 0
        elif csv_boost[j] <= 349:
            p = 1
        elif csv_boost[j] <= 399:
            p = 2
        elif csv_boost[j] <= 449:
            p = 3
        elif csv_boost[j] <= 499:
            p = 4
        else:
            p = 5

        if p in counts and counts[p] < 1 and balance:
            continue
        if p in counts:
            counts[p] = counts[p] - 1

        tmp = []
        for d in singleperf_benchmarks[i]:
            tmp += [d['y']]
        X_singleperf += [tmp[:50] + tmp[500:550] + tmp[1000:1050]]
        X_singleperf_boost += [tmp[25:75] + tmp[525:575] + tmp[1025:1075]]
        
        tmp1 = []
        for core in multiperf_benchmarks[i]:
            for d in core:
                tmp1 += [d['y']]
        
        tmp2 = []
        for i in range(20):
            tmp2 += [tmp1[i * 5000]]
        X_multiperf += [tmp2]

        X_combinedperf += [tmp + tmp2]

        y_boost += [p]

    return X_singleperf, X_multiperf, X_combinedperf, X_singleperf_boost, y_boost


def prepare_frequency_boost_cap(balance, db_models, singleperf_benchmarks, multiperf_benchmarks, csv_models, csv_models_r, csv_base, csv_boost):
    max_count = 19
    counts = {0 : max_count, 1 : max_count, 2 : max_count, 3 : max_count, 4 : max_count, 5 : max_count}
    
    X_singleperf = []
    X_multiperf = []
    X_singleperf_boost = []
    X_combinedperf = []
    y_boost_cap = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models:
            j = csv_models.index(db_model)
        elif db_model in csv_models_r:
            j = csv_models_r.index(db_model)
        else:
            continue
        
        boost_diff = csv_boost[j] - csv_base[j]
        if boost_diff <= 60:
            p = 0
        elif boost_diff <= 110:
            p = 1
        elif boost_diff <= 160:
            p = 2
        elif boost_diff <= 210:
            p = 3
        elif boost_diff <= 260:
            p = 4
        else:
            p = 5

        if p in counts and counts[p] < 1 and balance:
            continue
        if p in counts:
            counts[p] = counts[p] - 1

        tmp = []
        for d in singleperf_benchmarks[i]:
            tmp += [d['y']]
        X_singleperf += [tmp[:50] + tmp[500:550] + tmp[1000:1050]]
        X_singleperf_boost += [tmp[25:75] + tmp[525:575] + tmp[1025:1075]]
        
        tmp1 = []
        for core in multiperf_benchmarks[i]:
            for d in core:
                tmp1 += [d['y']]
        
        tmp2 = []
        for i in range(20):
            tmp2 += [tmp1[i * 5000]]
        X_multiperf += [tmp2]

        X_combinedperf += [tmp + tmp2]

        y_boost_cap += [p]

    return X_singleperf, X_multiperf, X_combinedperf, X_singleperf_boost, y_boost_cap


def prepare_boosttech(balance, db_models, singleperf_benchmarks, csv_models, csv_models_r, csv_base, csv_boost):
    max_count = 65
    counts = {True : max_count, False : max_count}

    X_boosttech = []
    y_boosttech = []

    for i, db_model in enumerate(db_models):
        j = -1
        if db_model in csv_models:
            j = csv_models.index(db_model)
        elif db_model in csv_models_r:
            j = csv_models_r.index(db_model)
            
        if j != -1:
            p = csv_base[j] != csv_boost[j]
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in singleperf_benchmarks[i]:
                tmp += [d['y']]
            #X_boosttech += [tmp[:50] + tmp[500:550] + tmp[1000:1050]]
            X_boosttech += [tmp[:50]]
            y_boosttech += [p]
    
    return X_boosttech, y_boosttech


def prepare_uarch(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_models, csv_models_r, csv_uarch):
    X_uarch = []
    y_uarch = []    
    uarchs = []

    for i, db_model in enumerate(db_models): 
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)
            
            uarchs += [csv_uarch[index]]

    counter = collections.Counter(uarchs).most_common(16) # was 10
    counter = dict(counter)
    counts = {k: 25 for k, v in counter.items()}
    # counts['Firestorm and Icestorm'] = 0

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)
            
            p = csv_uarch[index]
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []

            for d in cacheasso_benchmarks[i][:17:2]:
                tmp += [d['y']]

            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]

            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            for d in cores[i][:17]:
                tmp += [d['y']]
            
            X_uarch += [tmp]
            y_uarch += [p]

    return X_uarch, y_uarch


def prepare_uarch_grouped(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_models, csv_models_r, csv_uarch):
    X_uarch = []
    y_uarch = []
    csv_uarch = replace_uarch_by_base(csv_uarch)
    uarchs = []

    for i, db_model in enumerate(db_models): 
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)
            
            uarchs += [csv_uarch[index]]

    counter = collections.Counter(uarchs).most_common(10) # was 10
    counter = dict(counter)
    counts = {k: 22 for k, v in counter.items()}
    # counts['Firestorm and Icestorm'] = 0

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)
            
            p = csv_uarch[index]
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []

            for d in cacheasso_benchmarks[i][:17:2]:
                tmp += [d['y']]

            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]

            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            for d in cores[i][:17]:
                tmp += [d['y']]
            
            X_uarch += [tmp]
            y_uarch += [p]

    return X_uarch, y_uarch


def prepare_vendor(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, csv_models, csv_models_r):
    max_count = 165
    counts = {'ARM' : 0, 'AMD' : max_count, 'Intel' : max_count}

    X_vendor = []
    y_vendor = []

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            p = 'Intel' if 'Intel' in db_model else 'AMD' if 'AMD' in db_model else 'ARM'
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]
            # tmp += [cachesize_benchmarks_large[i][0]['y']]
            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            X_vendor += [tmp]
            y_vendor += [p]

    return X_vendor, y_vendor


def prepare_vendor_all(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, csv_models, csv_models_r):
    max_count = 20
    counts = {'ARM' : max_count, 'AMD' : max_count, 'Intel' : max_count}

    X_vendor = []
    y_vendor = []

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:            
            p = 'Intel' if 'Intel' in db_model else 'AMD' if 'AMD' in db_model else 'ARM'
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]
            # tmp += [cachesize_benchmarks_large[i][0]['y']]
            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            X_vendor += [tmp]
            y_vendor += [p]

    return X_vendor, y_vendor


def prepare_model_all(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, execution_times, csv_models, csv_models_r):
    X_model = []
    y_model = []

    p_models = []
    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and execution_times[i] != []:
            p_models += [db_model]

    counter = collections.Counter(p_models).most_common(14)
    counter = dict(counter)
    counts = {k: 9 for k, v in counter.items()}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1 and len(execution_times[i]) > 1:
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cacheasso_benchmarks[i][:17:2]:
                tmp += [d['y']]

            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]
            
            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]
            
            for d in cores[i][:17]:
                tmp += [d['y']]
            
            tmp += execution_times[i]
            
            X_model += [tmp]
            y_model += [p]
    
    return X_model, y_model


def prepare_model(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_models, csv_models_r):
    X_model = []
    y_model = []

    counter = collections.Counter(db_models).most_common(18)
    counter = dict(counter)
    counts = {k: 9 for k, v in counter.items()}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cacheasso_benchmarks[i][:17:2]:
                tmp += [d['y']]

            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]
            
            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            for d in cores[i][:17]:
                tmp += [d['y']]
            
            X_model += [tmp]
            y_model += [p]
    
    return X_model, y_model


def prepare_M1(balance, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_models, csv_models_r):
    X_model = []
    y_model = []

    # counter = collections.Counter(db_models).most_common(13)
    # counter = dict(counter)
    # counts = {k: 9 for k, v in counter.items()}

    counts = {'Apple M1' : 20, 'Other' : 20}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(cachesize_benchmarks_large[i]) > 1:
            p = 'Apple M1' if db_model == 'Apple M1' else 'Other'
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cacheasso_benchmarks[i][:17:2]:
                tmp += [d['y']]

            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]
            
            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            for d in cores[i][:17]:
                tmp += [d['y']]
            
            X_model += [tmp]
            y_model += [p]
    
    return X_model, y_model


def prepare_cpuvscpu(balance, a, b, db_models, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_models, csv_models_r):
    X_model = []
    y_model = []

    # counter = collections.Counter(db_models).most_common(13)
    # counter = dict(counter)
    # counts = {k: 9 for k, v in counter.items()}

    counts = {a : 20, b : 20}

    for i, db_model in enumerate(db_models):
        if (db_model == a or db_model == b) and len(cachesize_benchmarks_large[i]) > 1:
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cacheasso_benchmarks[i][:17:2]:
                tmp += [d['y']]

            for d in cachesize_benchmarks_small[i][3::2]:
                tmp += [d['y']]
            
            for d in cachesize_benchmarks_large[i]:
                tmp += [d['y']]
            
            for d in tlb_benchmarks[i][::2]:
                tmp += [d['y']]

            for d in cores[i][:17]:
                tmp += [d['y']]
            
            X_model += [tmp]
            y_model += [p]
    
    return X_model, y_model


def prepare_cpuvscpu_execution(balance, a, b, db_models, execution_times, csv_models, csv_models_r):
    X_model = []
    y_model = []

    # counter = collections.Counter(db_models).most_common(13)
    # counter = dict(counter)
    # counts = {k: 9 for k, v in counter.items()}

    counts = {a : 20, b : 20}

    for i, db_model in enumerate(db_models):
        if (db_model == a or db_model == b) and len(execution_times[i]) > 1:
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            X_model += [execution_times[i]]
            y_model += [p]
    
    return X_model, y_model


def prepare_singleintel(balance, db_models, execution_times, csv_models, csv_models_r):
    X_model = []
    y_model = []

    # counter = collections.Counter(db_models).most_common(13)
    # counter = dict(counter)
    # counts = {k: 9 for k, v in counter.items()}

    counts = {'Intel(R) Core(TM) i5-8250U' : 20, 'Other' : 20}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and execution_times[i] != []:
            p = 'Intel(R) Core(TM) i5-8250U' if db_model == 'Intel(R) Core(TM) i5-8250U' else 'Other'
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1
            
            X_model += [execution_times[i]]
            y_model += [p]
    
    return X_model, y_model


def prepare_othermodel(balance, db_models, singleperf_benchmarks, cores, csv_models, csv_models_r):
    counter = collections.Counter(db_models).most_common(19)
    counter = dict(counter)
    
    X_othermodel = []
    y_othermodel = []

    counts = {k: 7 for k, v in counter.items()}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r):            
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            # for d in singleperf_benchmarks[i]:
            #     tmp += [d['y']]
            # tmp = tmp[:25] + tmp[500:525] + tmp[1000:1025]
            for d in cores[i][:17]:
                tmp += [d['y']]

            X_othermodel += [tmp]
            y_othermodel += [p]

    return X_othermodel, y_othermodel


def prepare_model_execution(balance, db_models, execution_times, cachesize_benchmarks_large, csv_models, csv_models_r):
    X_othermodel = []
    y_othermodel = []

    p_models = []
    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and execution_times[i] != [] and len(cachesize_benchmarks_large[i]) > 1:
            p_models += [db_model]

    counter = collections.Counter(p_models).most_common(14)
    counter = dict(counter)
    counts = {k: 9 for k, v in counter.items()}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and execution_times[i] != [] and len(cachesize_benchmarks_large[i]) > 1:
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            X_othermodel += [execution_times[i]]
            y_othermodel += [p]

    return X_othermodel, y_othermodel


def prepare_model_timer(balance, db_models, timer, csv_models, csv_models_r):
    X_othermodel = []
    y_othermodel = []

    p_models = []
    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(timer[i]) == 3:
            p_models += [db_model]

    counter = collections.Counter(p_models).most_common(19)
    counter = dict(counter)
    counts = {k: 7 for k, v in counter.items()}

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and len(timer[i]) == 3:
            p = db_model
            if p not in counts:
                continue
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in timer[i]:
                tmp += [d['y']]

            X_othermodel += [tmp]
            y_othermodel += [p]

    return X_othermodel, y_othermodel


def prepare_tlb(balance, db_models, tlb_benchmarks, csv_models, csv_models_r, csv_tlb):
    X_tlb = []
    y_tlb = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models or db_model in csv_models_r:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)
            y_tlb += [csv_tlb[index]]
            tmp = []
            for d in tlb_benchmarks[i]:
                tmp += [d['y']]
            X_tlb += [tmp]

    return X_tlb, y_tlb


def prepare_threads(balance, db_models, cores, csv_models, csv_models_r, csv_threads):
    max_count = 40
    counts = {2 : max_count, 4 : max_count, 6 : max_count, 8 : max_count, 12 : max_count, 16 : max_count, 20 : max_count, 24 : 0}

    X_threads = []
    y_threads = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models or db_model in csv_models_r:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)

            p = int(csv_threads[index])
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cores[i][:17]:
                tmp += [d['y']]
            X_threads += [tmp]
            y_threads += [p]

    return X_threads, y_threads


def prepare_htt(balance, db_models, cores, csv_models, csv_models_r, csv_smt):
    max_count = 139
    counts = {False : max_count, True : max_count}

    X_htt = []
    y_htt = []

    for i, db_model in enumerate(db_models):
        if (db_model in csv_models or db_model in csv_models_r) and 'Intel' in db_model:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)

            p = csv_smt[index]
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cores[i][:17]:
                tmp += [d['y']]
            X_htt += [tmp]
            y_htt += [p]

    return X_htt, y_htt


def prepare_smt(balance, db_models, cores, csv_models, csv_models_r, csv_smt):
    max_count = 210
    counts = {False : max_count, True : max_count}

    X_smt = []
    y_smt = []

    for i, db_model in enumerate(db_models):
        if db_model in csv_models or db_model in csv_models_r:
            try:
                index = csv_models.index(db_model)
            except:
                index = csv_models_r.index(db_model)

            p = csv_smt[index]
            if p in counts and counts[p] < 1 and balance:
                continue
            if p in counts:
                counts[p] = counts[p] - 1

            tmp = []
            for d in cores[i][:17]:
                tmp += [d['y']]
            X_smt += [tmp]
            y_smt += [p]

    return X_smt, y_smt