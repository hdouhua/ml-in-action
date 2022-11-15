# hack module search path
# import sys
# sys.path.append(".")
# print(sys.path)

import gzip

from joblib import dump
from sklearn import datasets
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from app.config import MODEL_FILE

iris = datasets.load_iris(return_X_y=True)
y = iris[1]
X = iris[0]

clf_pipeline = [('scaling', MinMaxScaler()), ('clf', GradientBoostingClassifier())]
pipeline = Pipeline(clf_pipeline)

pipeline.fit(X, y)

dump(pipeline, gzip.open(MODEL_FILE, "wb"))
