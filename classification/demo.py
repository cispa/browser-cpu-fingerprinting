import warnings

from utils import *

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedKFold, KFold
from sklearn import metrics
from joblib import dump

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
    'svc__gamma': [1e-2, 1e-4, 1e-6, 1e-8, 'scale', 'auto'],
    'svc__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
}

mlp_parameters = {
    'mlpclassifier__hidden_layer_sizes': [(50, 50, 50), (50, 100, 50), (100,)],
    'mlpclassifier__activation': ['tanh', 'relu'],
    'mlpclassifier__solver': ['sgd', 'adam'],
    'mlpclassifier__alpha': [0.0001, 0.05],
    'mlpclassifier__learning_rate': ['constant', 'adaptive'],
}

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
        make_pipeline(preprocessor, SVC(probability=True)),
        param_grid=svc_parameters,
        cv=cv, n_jobs=-1)
]
classifiers += [
    GridSearchCV(
        make_pipeline(preprocessor, MLPClassifier()),
        param_grid=mlp_parameters,
        cv=cv, n_jobs=-1)
]


def iterate_classifiers(classifiers, target, X, y):
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
            make_pipeline(preprocessor, SVC(probability=True)),
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
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        print(f"Test Size: {len(X_test)}")

        max_accuracy = 0.0
        max_index = -1
        for i, classifier in enumerate(classifiers):
            print(f"Iteration {i+1} / {len(classifiers)}")
            classifier.fit(X_train, y_train)
            y_predict = classifier.predict(X_test)
            accuracy = metrics.accuracy_score(y_test, y_predict)
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                max_index = i
            print(f"ACC - {accuracy}")
            print(
                f"F1  - {metrics.f1_score(y_test, y_predict, average='macro')}")
        dump(classifiers[max_index], Path(
            '.cache/classifiers/' + target.replace(" ", "") + '.dump'))
        print("")


# load database and csv
db_models, benchmarks = load_database()
csv_dict = load_csv()

# preparing data
print('[-]  Preparing data')

# reduce execution times to just 5
benchmarks['execution_times'] = list(map(lambda x: [x[2], x[3],
                                                    x[4], x[5], x[12]] if len(x) > 0 else [], benchmarks['execution_times']))
X_l1, y_l1 = prepare_l1(
    balance, db_models, benchmarks['cachesize_benchmarks_small'], csv_dict['name'], csv_dict['rname'], csv_dict['l1'])
X_l2, y_l2large = prepare_l2(balance, db_models, benchmarks['cachesize_benchmarks_small'],
                             benchmarks['cachesize_benchmarks_large'], csv_dict['name'], csv_dict['rname'], csv_dict['l2'])
X_l3, y_l3 = prepare_l3(balance, db_models, benchmarks['cachesize_benchmarks_small'],
                        benchmarks['cachesize_benchmarks_large'], csv_dict['name'], csv_dict['rname'], csv_dict['l3'])
X_l1asso, y_l1asso = prepare_l1asso(
    balance, db_models, benchmarks['cacheasso_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['l1asso'])
X_tlb, y_tlb = prepare_tlb(
    balance, db_models, benchmarks['tlb_benchmarks'], csv_dict['name'], csv_dict['rname'], csv_dict['tlb'])
X_threads, y_threads = prepare_threads(
    balance, db_models, benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['threads'])
X_uarch, y_uarch = prepare_uarch(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'],
                                 benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['uarch'])
X_uarch_grouped, y_uarch_grouped = prepare_uarch_grouped(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks[
                                                         'tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'], csv_dict['uarch'])
X_vendor, y_vendor = prepare_vendor(balance, db_models, benchmarks['cachesize_benchmarks_small'],
                                    benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], csv_dict['name'], csv_dict['rname'])
X_vendor_all, y_vendor_all = prepare_vendor_all(
    balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks['tlb_benchmarks'], csv_dict['name'], csv_dict['rname'])
X_model, y_model = prepare_model(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'],
                                 benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])
X_model_all, y_model_all = prepare_model_all(balance, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'], benchmarks[
                                             'tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], benchmarks['execution_times'], csv_dict['name'], csv_dict['rname'])
X_othermodel_execution, y_othermodel_execution = prepare_model_execution(
    balance, db_models, benchmarks['execution_times'], benchmarks['cachesize_benchmarks_large'], csv_dict['name'], csv_dict['rname'])
X_m1, y_m1 = prepare_M1(False, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'],
                        benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])

# running algorithms

print('[-]  Running algorithms')

# iterate

iterate_classifiers(classifiers, 'L1 Cache Sizes', X_l1, y_l1)
iterate_classifiers(classifiers, 'L2 Cache Sizes', X_l2, y_l2large)
iterate_classifiers(classifiers, 'L3 Cache Sizes', X_l3, y_l3)
iterate_classifiers(classifiers, 'L1 Associativities', X_l1asso, y_l1asso)
iterate_classifiers(classifiers, 'L1D TLB Sizes', X_tlb, y_tlb)
iterate_classifiers(classifiers, 'Number of Threads', X_threads, y_threads)

# iterate
iterate_classifiers(classifiers, 'AMD vs Intel', X_vendor, y_vendor)
iterate_classifiers(classifiers, 'ARM vs Intel vs AMD',
                    X_vendor_all, y_vendor_all)
iterate_classifiers(classifiers, 'M1 vs Rest', X_m1, y_m1)
iterate_classifiers(
    classifiers, 'Models with a lot of benchmarks', X_model, y_model)
iterate_classifiers(classifiers, 'Models with execution times',
                    X_othermodel_execution, y_othermodel_execution)
iterate_classifiers(classifiers, 'Models with everything',
                    X_model_all, y_model_all)
iterate_classifiers(classifiers, 'Microarchitectures', X_uarch, y_uarch)
iterate_classifiers(classifiers, 'Microarchitectures grouped by design',
                    X_uarch_grouped, y_uarch_grouped)

print('\n[+]  DONE')
