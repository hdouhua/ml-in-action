# hack module search path
# import sys
# sys.path.append(".")
# print(sys.path)

from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingClassifier
from joblib import dump
import gzip
from config import model_file

iris = datasets.load_iris(return_X_y=True)
y = iris[1]
X = iris[0]

clf_pipeline = [('scaling', MinMaxScaler()),
                ('clf', GradientBoostingClassifier())]
pipeline = Pipeline(clf_pipeline)

pipeline.fit(X, y)

dump(pipeline, gzip.open(model_file, "wb"))
