import warnings
from utils import *
from joblib import load
from sklearn import metrics

# load database and csv
db_models, benchmarks = load_database()
csv_dict = load_csv()
balance = True

# preparing data
print('[-]  Preparing data')

# reduce execution times to just 5
benchmarks['execution_times'] = list(map(lambda x: [x[2], x[3],
                                                    x[4], x[5], x[12]] if len(x) > 0 else [], benchmarks['execution_times']))
X_m1, y_m1 = prepare_M1(False, db_models, benchmarks['cachesize_benchmarks_small'], benchmarks['cachesize_benchmarks_large'],
                        benchmarks['tlb_benchmarks'], benchmarks['cacheasso_benchmarks'], benchmarks['cores'], csv_dict['name'], csv_dict['rname'])

classifier = load(Path('.cache/classifiers/M1vsRest.dump'))
y_predict = classifier.predict(X_m1[:200])
print(y_predict)
print(metrics.accuracy_score(y_m1[:200], y_predict))
print(classifier.predict_proba(X_m1[:10]))

print('\n[+]  DONE')
