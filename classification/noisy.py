import warnings
import sqlite3
import json

from utils import *

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedKFold, KFold
from sklearn import metrics

balance = True
# cv = RepeatedKFold(n_splits=5, n_repeats=5, random_state=1)
cv = KFold(n_splits=5)
preprocessor = StandardScaler()

dummy_parameters = {
    'dummyclassifier__strategy': ['uniform']
}

kn_parameters = {
    'kneighborsclassifier__n_neighbors': [i for i in range(2, 9)],
    'kneighborsclassifier__weights': ['uniform', 'distance']
}

svc_parameters = {
    'svc__kernel': ['rbf'],
    'svc__gamma' : [1e-2, 1e-4, 1e-6, 1e-8, 'scale', 'auto'],
    'svc__C' : [0.001, 0.01, 0.1, 1, 10, 100, 1000],
}

mlp_parameters = {
    'mlpclassifier__hidden_layer_sizes': [(50,50,50), (50,100,50), (100,)],
    'mlpclassifier__activation': ['tanh', 'relu'],
    'mlpclassifier__solver': ['sgd', 'adam'],
    'mlpclassifier__alpha': [0.0001, 0.05],
    'mlpclassifier__learning_rate': ['constant', 'adaptive'],
}

classifiers = []
classifiers += [
    GridSearchCV(
        make_pipeline(preprocessor, DummyClassifier()),
        param_grid=dummy_parameters,
        cv=cv, n_jobs=-1)
]
classifiers += [
    GridSearchCV(
        make_pipeline(preprocessor, KNeighborsClassifier()),
        param_grid=kn_parameters,
        cv=cv, n_jobs=-1)
]
classifiers += [
    GridSearchCV(
        make_pipeline(preprocessor, SVC()),
        param_grid=svc_parameters,
        cv=cv, n_jobs=-1)
]
classifiers += [
    GridSearchCV(
        make_pipeline(preprocessor, MLPClassifier()),
        param_grid=mlp_parameters,
        cv=cv, n_jobs=-1)
]


db_models_test = []
cacheasso_benchmarks = []
cachesize_benchmarks_small = []
cachesize_benchmarks_large = []
tlb_benchmarks = []
timer_diff = []
singleperf_benchmarks = []
cores = []
execution_times = []

def load_test_data():
    global db_models_test, execution_times, cacheasso_benchmarks, cachesize_benchmarks_small, cachesize_benchmarks_large
    global tlb_benchmarks, timer_diff, singleperf_benchmarks, cores
    con = sqlite3.connect('/path/to/db_noisy.sqlite3')
    cursor = con.execute("SELECT * FROM upload_benchmarkresult;")
    for row in cursor.fetchall():
        db_models_test += [row[1]]
        execution_times += [json.loads(row[5])]
        benchmarks = json.loads(row[3])
        cacheasso_benchmarks += [benchmarks[2]]
        cachesize_benchmarks_small += [benchmarks[3]]
        cachesize_benchmarks_large += [benchmarks[4]]
        tlb_benchmarks += [benchmarks[5]]
        timer_diff += [benchmarks[7][:4]]
        singleperf_benchmarks += [benchmarks[10]]
        cores += [benchmarks[12]]


def iterate_classifiers(classifiers, target, X, y, X_test, y_test):
    classifiers = []
    classifiers += [
        DummyClassifier(strategy="uniform"),
        DummyClassifier(strategy="most_frequent"),
    ]
    classifiers += [
        GridSearchCV(
            make_pipeline(preprocessor, KNeighborsClassifier()),
            param_grid=kn_parameters,
            cv=cv, n_jobs=-1)
    ]
    classifiers += [
        GridSearchCV(
            make_pipeline(preprocessor, SVC()),
            param_grid=svc_parameters,
            cv=cv, n_jobs=-1)
    ]
    classifiers += [
        GridSearchCV(
            make_pipeline(preprocessor, MLPClassifier()),
            param_grid=mlp_parameters,
            cv=cv, n_jobs=-1)
    ]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print(target)
        X_train, _, y_train, _ = train_test_split(X, y)
        print(f"Test Size: {len(X_test)}")
        for i, classifier in enumerate(classifiers):
            print(f"Iteration {i+1} / {len(classifiers)}")
            classifier.fit(X_train, y_train)
            y_predict = classifier.predict(X_test)
            acc = metrics.accuracy_score(y_test, y_predict)
            print(acc)
        print("")


# load database and csv
db_models, benchmarks = load_database()
csv_dict = load_csv()

# preparing data
print('[-]  Preparing data')

X_l1, y_l1 = prepare_l1(balance, db_models, benchmarks['cachesize_benchmarks_small'], csv_dict['name'], csv_dict['rname'], csv_dict['l1'])
X_l2, y_l2large = prepare_l2(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], csv_dict['name'], csv_dict['rname'], csv_dict['l2'])
X_l3, y_l3 = prepare_l3(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], csv_dict['name'], csv_dict['rname'], csv_dict['l3'])
X_l1asso, y_l1asso = prepare_l1asso(balance, db_models, benchmarks['cacheasso_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['l1asso'])
X_tlb, y_tlb = prepare_tlb(balance, db_models, benchmarks['tlb_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['tlb'])
X_threads, y_threads = prepare_threads(balance, db_models, benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['threads'])
X_htt, y_htt = prepare_htt(balance, db_models, benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['smt'])
X_smt, y_smt = prepare_smt(balance, db_models, benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['smt'])
# X_singleperf_base, X_multiperf_base, X_combinedperf_base, _ , y_base = prepare_frequency_base(balance, db_models, benchmarks['singleperf_benchmarks'], benchmarks['multiperf_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['base'])
# X_singleperf_boost, X_multiperf_boost, X_combinedperf_boost, X_singleperf_boost2, y_boost = prepare_frequency_boost(balance, db_models, benchmarks['singleperf_benchmarks'], benchmarks['multiperf_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['boost'])
# X_singleperf_boost_cap, X_multiperf_boost_cap, X_combinedperf_boost_cap, X_singleperf_boost_cap2, y_boost_cap = prepare_frequency_boost_cap(balance, db_models, benchmarks['singleperf_benchmarks'], benchmarks['multiperf_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['base'], csv_dict['boost'])
X_boosttech, y_boosttech = prepare_boosttech(balance, db_models, benchmarks['singleperf_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['base'], csv_dict['boost'])
X_uarch, y_uarch = prepare_uarch(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['uarch'])
X_uarch_grouped, y_uarch_grouped = prepare_uarch_grouped(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['uarch'])
X_vendor, y_vendor = prepare_vendor(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], csv_dict['name'], csv_dict['rname'])
X_vendor_all, y_vendor_all = prepare_vendor_all(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], csv_dict['name'], csv_dict['rname'])
X_model, y_model = prepare_model(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])
X_model_all, y_model_all = prepare_model_all(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], benchmarks['execution_times'], csv_dict['name'], csv_dict['rname'])
X_othermodel, y_othermodel = prepare_othermodel(balance, db_models, benchmarks['singleperf_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])
X_othermodel_execution, y_othermodel_execution = prepare_model_execution(balance, db_models, benchmarks['execution_times'], benchmarks['cachesize_benchmarks_large'], csv_dict['name'], csv_dict['rname'])
X_othermodel_timer, y_othermodel_timer = prepare_model_timer(balance, db_models, benchmarks['timer'], csv_dict['name'], csv_dict['rname'])
X_m1, y_m1 = prepare_M1(False, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])
X_singleintel, y_singleintel = prepare_singleintel(False, db_models, benchmarks['execution_times'], csv_dict['name'], csv_dict['rname'])
X_intelvintel, y_intelvintel = prepare_cpuvscpu(False, 'Intel(R) Core(TM) i5-8250U', 'Intel(R) Core(TM) i7-8550U', db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])
X_amdvamd, y_amdvamd = prepare_cpuvscpu(False, 'AMD Ryzen 5 2600', 'AMD Ryzen 5 3600', db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])
X_intelvintel_execution, y_intelvintel_execution = prepare_cpuvscpu_execution(False, 'Intel(R) Core(TM) i5-8250U', 'Intel(R) Core(TM) i7-8550U', db_models, benchmarks['execution_times'], csv_dict['name'], csv_dict['rname'])

print('[-]  Preparing test data')

load_test_data()
db_models_test = model_filter(db_models_test)

X_l1_test, y_l1_test = prepare_l1(False, db_models_test, cachesize_benchmarks_small, csv_dict['name'], csv_dict['rname'], csv_dict['l1'])
X_l2_test, y_l2large_test = prepare_l2(False, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, csv_dict['name'], csv_dict['rname'], csv_dict['l2'])
X_l3_test, y_l3_test = prepare_l3(False, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, csv_dict['name'], csv_dict['rname'], csv_dict['l3'])
X_l1asso_test, y_l1asso_test = prepare_l1asso(False, db_models_test, cacheasso_benchmarks, csv_dict['name'], csv_dict['rname'], csv_dict['l1asso'])
X_tlb_test, y_tlb_test = prepare_tlb(False, db_models_test, tlb_benchmarks, csv_dict['name'], csv_dict['rname'], csv_dict['tlb'])
X_threads_test, y_threads_test = prepare_threads(False, db_models_test, cores, csv_dict['name'], csv_dict['rname'], csv_dict['threads'])
X_htt_test, y_htt_test = prepare_htt(False, db_models_test, cores, csv_dict['name'], csv_dict['rname'], csv_dict['smt'])
X_smt_test, y_smt_test = prepare_smt(False, db_models_test, cores, csv_dict['name'], csv_dict['rname'], csv_dict['smt'])

X_boosttech_test, y_boosttech_test = prepare_boosttech(False, db_models_test, singleperf_benchmarks, csv_dict['name'], csv_dict['rname'], csv_dict['base'], csv_dict['boost'])
X_uarch_test, y_uarch_test = prepare_uarch(False, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_dict['name'], csv_dict['rname'], csv_dict['uarch'])
X_uarch_grouped_test, y_uarch_grouped_test = prepare_uarch_grouped(False, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_dict['name'], csv_dict['rname'], csv_dict['uarch'])
X_vendor_test, y_vendor_test = prepare_vendor(True, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, csv_dict['name'], csv_dict['rname'])
X_model_all_test, y_model_all_test = prepare_model_all(False, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, execution_times, csv_dict['name'], csv_dict['rname'])
X_m1_test, y_m1_test = prepare_M1(False, db_models_test, cachesize_benchmarks_small, cachesize_benchmarks_large, tlb_benchmarks, cacheasso_benchmarks, cores, csv_dict['name'], csv_dict['rname'])

# running algorithms

print('[-]  Running algorithms')

iterate_classifiers(classifiers, 'L1 Cache Sizes', X_l1, y_l1, X_l1_test, y_l1_test)
iterate_classifiers(classifiers, 'L2 Cache Sizes', X_l2, y_l2large, X_l2_test, y_l2large_test)
iterate_classifiers(classifiers, 'L3 Cache Sizes', X_l3, y_l3, X_l3_test, y_l3_test)
iterate_classifiers(classifiers, 'L1 Associativities', X_l1asso, y_l1asso, X_l1asso_test, y_l1asso_test)
iterate_classifiers(classifiers, 'L1D TLB Sizes', X_tlb, y_tlb, X_tlb_test, y_tlb_test)
iterate_classifiers(classifiers, 'Number of Threads', X_threads, y_threads, X_threads_test, y_threads_test)
iterate_classifiers(classifiers, 'HTT Availability', X_htt, y_htt, X_htt_test, y_htt_test)
iterate_classifiers(classifiers, 'SMT Availability', X_smt, y_smt, X_smt_test, y_smt_test)
iterate_classifiers(classifiers, 'Boost Technology Availability', X_boosttech, y_boosttech, X_boosttech_test, y_boosttech_test)

# iterate_classifiers(classifiers, 'AMD vs Intel', X_vendor, y_vendor, X_vendor_test, y_vendor_test)
# iterate_classifiers(classifiers, 'Models with everything', X_model_all, y_model_all, X_model_all_test, y_model_all_test)
# iterate_classifiers(classifiers, 'Microarchitectures', X_uarch, y_uarch, X_uarch_test, y_uarch_test)
# iterate_classifiers(classifiers, 'Microarchitectures grouped by design', X_uarch_grouped, y_uarch_grouped, X_uarch_grouped_test, y_uarch_grouped_test)
# iterate_classifiers(classifiers, 'M1 vs Rest', X_m1, y_m1, X_m1_test, y_m1_test)

print('\n[+]  DONE')