# -*- coding: utf-8 -*-
"""Semana7_G4_TalentoTech.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kpRl6bGdIhaPkImqZuVsRdWAJ9guLxtx

# Análisis de datos de base de datos agrícola

## Regresión
"""

import pandas as pd
db = pd.read_csv('/content/forestfires.csv')
db.head()

db.info()

db.keys()

from sklearn.preprocessing import LabelEncoder
db_encoded = db.copy() # Guardar un BackUp
for label in ['month','day']:
  db_encoded[label] = LabelEncoder().fit_transform(db_encoded[label])

db_encoded.head()
#Hacer la conversión de meses y días con diccionario! January-->0, Monday-->0

caracteristicas = db_encoded[['X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH','wind', 'rain']].values
target = db_encoded['area'].values

# Commented out IPython magic to ensure Python compatibility.
# %whos

"""## Árboles de Decisión
![](https://github.com/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/figures/05.08-decision-tree.png?raw=1)
"""

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
reg_tree = DecisionTreeRegressor().fit(caracteristicas,target)
reg_tree

reg_tree.get_params()

target_predecido = reg_tree.predict(caracteristicas)
target_predecido

target_predecido[200:210], target[200:210]

from sklearn.metrics import mean_squared_error
mean_squared_error(target, target_predecido)

import matplotlib.pyplot as plt
import numpy as np
eje_x = np.array(range(db.shape[0]))
plt.scatter(eje_x,target,marker='.')
plt.scatter(eje_x,target_predecido,marker='.',color='hotpink')

"""## Vamos a dividir el conjunto en entrenamiento y prueba!"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(caracteristicas, target, test_size=0.3, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

reg_tree2 = DecisionTreeRegressor().fit(X_train,y_train)
reg_tree2

"""## Prediciendo en conjunto de entrenamiento"""

pred_train = reg_tree2.predict(X_train)
mean_squared_error(y_train, pred_train)

import matplotlib.pyplot as plt
import numpy as np
eje_x2 = np.array(range(np.shape(y_train)[0]))
plt.scatter(eje_x2,y_train,marker='.')
plt.scatter(eje_x2,pred_train,marker='.',color='Yellow')

"""## Prediciendo en conjunto de prueba"""

pred_test = reg_tree2.predict(X_test)
mean_squared_error(y_test, pred_test)

import matplotlib.pyplot as plt
import numpy as np
eje_x3 = np.array(range(np.shape(y_test)[0]))
plt.scatter(eje_x3,y_test,marker='.')
plt.scatter(eje_x3,pred_test,marker='.',color='Yellow')

"""## Visualizaciones sobre periodos de incendios"""

db.head()

import seaborn as sns
ax = sns.boxplot(data=db, x="month", y="area")
ax.set_ylim(0, 200)

import seaborn as sns
ax = sns.boxplot(data=db, x="month", y="rain")
ax.set_ylim(0, 1)

import seaborn as sns
ax = sns.boxplot(data=db, x="month", y="wind")
#ax.set_ylim(0, 1)

"""1. Buscar una forma de visualizar las lluvias. Sumen valores por mes!
2. Analizar Temperatura y RH
3. Explorar otros parámetros para el regresor y mejorar lo obtenido en el conjunto de prueba
4. Cambiar la escala!

# Cambiar la escala a logarítmica?
"""

db.head()

db['area'].min(), db['area'].max()

np.log(1)

"""## Vamos a dividir el conjunto en entrenamiento y prueba!"""

target[200:220], np.log(target+1)[200:220]

from sklearn.model_selection import train_test_split
target_log = np.log(target+1)
X_train, X_test, y_train, y_test = train_test_split(caracteristicas, target_log, test_size=0.3, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

reg_tree2 = DecisionTreeRegressor(max_depth=10).fit(X_train,y_train)
reg_tree2

"""## Prediciendo en conjunto de entrenamiento"""

pred_train = reg_tree2.predict(X_train)
mean_squared_error(y_train, pred_train)

import matplotlib.pyplot as plt
import numpy as np
eje_x2 = np.array(range(np.shape(y_train)[0]))
plt.scatter(eje_x2,y_train,marker='.')
plt.scatter(eje_x2,pred_train,marker='.',color='Yellow')

"""## Prediciendo en conjunto de prueba"""

pred_test = reg_tree2.predict(X_test)
mean_squared_error(y_test, pred_test)

import matplotlib.pyplot as plt
import numpy as np
eje_x3 = np.array(range(np.shape(y_test)[0]))
plt.scatter(eje_x3,y_test,marker='.')
plt.scatter(eje_x3,pred_test,marker='.',color='Yellow')

eje_x3 = np.array(range(np.shape(y_test)[0]))
plt.scatter(eje_x3[0:40],y_test[0:40],marker='.')
plt.scatter(eje_x3[0:40],pred_test[0:40],marker='.',color='Yellow')

"""## Creando nuestra GridSearch"""

# Commented out IPython magic to ensure Python compatibility.
from sklearn.model_selection import GridSearchCV
param_grid = {'max_depth':[5,10,20,30,40,50,60,70,80,90,100,200,300,400,500]}
reg_tree2 = DecisionTreeRegressor().fit(X_train,y_train)
grid = GridSearchCV(reg_tree2, param_grid, cv=4, verbose=2,scoring='r2')
# %time grid.fit(X_train, y_train)
print(grid.best_params_)
print(grid.best_score_)
print(grid.best_index_)

"""# Usando DecisionTree como Clasificador"""

import pandas as pd
df0 = pd.read_csv('/content/onehr.data', header=None)
df1 = pd.read_csv('/content/eighthr.data', header=None)
df0.shape, df1.shape

df0.head()

np.unique(df0[73])

np.sum(df0[73])

df0[73].value_counts()

del df0[df0.columns[0]]

df0.info()

df0.replace('?',np.nan, inplace=True)

df0.dropna(inplace=True)

df0.head()

df0.shape

target = df0[73].values
caracteristicas = df0.iloc[:,1:5]

clf_tree = DecisionTreeClassifier().fit(caracteristicas,target)
clf_tree

y_pred = clf_tree.predict(caracteristicas)

target

from sklearn.metrics import confusion_matrix
confusion_matrix(target, y_pred)

X_train, X_test, y_train, y_test = train_test_split(caracteristicas, target, test_size=0.3, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

clf_tree2 = DecisionTreeClassifier(max_depth=3).fit(X_train,y_train)
clf_tree2

y_pred_tr = clf_tree.predict(X_train)
confusion_matrix(y_train, y_pred_tr)

y_pred_te = clf_tree.predict(X_test)
confusion_matrix(y_test, y_pred_te)

from IPython.display import Image
import pydotplus
from six import StringIO
from sklearn import tree
dot_data = StringIO()
tree.export_graphviz(clf_tree, out_file=dot_data)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())

"""## Probando con la base de datos de Iris"""

import seaborn as sns
import matplotlib.pyplot as plt
dts= sns.load_dataset("iris")

from sklearn.datasets import load_iris
import numpy as np
iris = load_iris()
X = iris.data
y = iris.target

iris.feature_names

X.shape, y.shape

y

from sklearn.tree import DecisionTreeClassifier
clf_tree = DecisionTreeClassifier(max_depth=2).fit(X,y)
clf_tree

from IPython.display import Image
import pydotplus
from six import StringIO
from sklearn import tree
dot_data = StringIO()
tree.export_graphviz(clf_tree, out_file=dot_data)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())

import matplotlib.pyplot as plt
plt.scatter(X[:,2], X[:,3], marker='^', c=y)

"""# Usando el Clasificador de Bosques Aleatorios

![](https://cdn-images-1.medium.com/max/1600/1*Wf91XObaX2zwow7mMwDmGw.png)
"""

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
model = RandomForestClassifier(n_estimators=5, random_state=1)

model.fit(X,y)

y_pred = model.predict(X)

y_pred[120:], y[120:]

from sklearn.metrics import confusion_matrix
confusion_matrix(y, y_pred)

model.feature_importances_

from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, random_state=10)
Xtrain.shape, ytrain.shape, Xtest.shape, ytest.shape

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
model = RandomForestClassifier(n_estimators=5, random_state=1)

model.fit(Xtrain,ytrain)

# Probando sobre el conjunto de entrenamiento
from sklearn.metrics import confusion_matrix
y_pred_tr = model.predict(Xtrain)
confusion_matrix(ytrain, y_pred_tr)

# Probando sobre el conjunto de prueba
from sklearn.metrics import confusion_matrix
y_pred_te = model.predict(Xtest)
confusion_matrix(ytest, y_pred_te)

model.score(Xtrain,ytrain),model.score(Xtest,ytest)

# Commented out IPython magic to ensure Python compatibility.
# Haciendo GridSearch con Xtrain - ytrain
from sklearn.model_selection import GridSearchCV
param_grid = {'n_estimators':[2,3,4,5,6,7,8,9,10,20,40,60,80,100,1000]}
grid = GridSearchCV(model, param_grid, cv=3, verbose=2, scoring='accuracy')

# %time grid.fit(Xtrain, ytrain)
print(grid.best_params_)
print(grid.best_score_)
print(grid.best_index_)

model = RandomForestClassifier(n_estimators=7, random_state=1)

model.fit(Xtrain, ytrain)

# Probando sobre el conjunto de entrenamiento
from sklearn.metrics import confusion_matrix
y_pred_tr = model.predict(Xtrain)
confusion_matrix(ytrain, y_pred_tr)

# Probando sobre el conjunto de prueba
from sklearn.metrics import confusion_matrix
y_pred_te = model.predict(Xtest)
confusion_matrix(ytest, y_pred_te)

model.score(Xtrain,ytrain),model.score(Xtest,ytest)

"""## Clasificadores Lineales"""

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(C=10, random_state=10)

lr.fit(Xtrain, ytrain)

# Prediciendo en conjunto de entrenamiento
y_pred_tr = lr.predict(Xtrain)
confusion_matrix(ytrain, y_pred_tr)

# Prediciendo en conjunto de prueba
y_pred_te = lr.predict(Xtest)
confusion_matrix(ytest, y_pred_te)

lr.score(Xtrain,ytrain),lr.score(Xtest,ytest)

from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(Xtrain, ytrain)

# Prediciendo en conjunto de entrenamiento
y_pred_tr = nb.predict(Xtrain)
confusion_matrix(ytrain, y_pred_tr)

# Prediciendo en conjunto de prueba
y_pred_te = nb.predict(Xtest)
confusion_matrix(ytest, y_pred_te)

nb.score(Xtrain,ytrain),nb.score(Xtest,ytest)

"""## Usando Regresores Lineales"""

from sklearn.datasets import load_wine
import numpy as np
vinos = load_wine()
wine = vinos.data

X = wine[:,1:]
y = wine[:,0]

vinos.feature_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_train.shape, X_test.shape, y_train.shape, y_test.shape

from sklearn.ensemble import RandomForestRegressor
rf_reg = RandomForestRegressor().fit(X_train, y_train)

y_pred_tr = rf_reg.predict(X_train)

y_pred_tr[0:20], y_train[0:20]

# Prediciendo en conjunto de prueba
y_pred_te = rf_reg.predict(X_test)

y_pred_te[0:20], y_test[0:20]

# visualizando estimaciones en entrenamiento
eje_x = np.array(range(X_train.shape[0]))
plt.scatter(eje_x,y_train,marker='.')
plt.scatter(eje_x,y_pred_tr,marker='x',color='hotpink')

# visualizando estimaciones en prueba
eje_x = np.array(range(X_test.shape[0]))
plt.scatter(eje_x,y_test,marker='.')
plt.scatter(eje_x,y_pred_te,marker='x',color='hotpink')

# Calculando MSE en entrenamiento
from sklearn.metrics import mean_squared_error
mean_squared_error(y_train, y_pred_tr)

# Calculando MSE en entrenamiento
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test, y_pred_te)

# Montar el LinearRegression
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression

