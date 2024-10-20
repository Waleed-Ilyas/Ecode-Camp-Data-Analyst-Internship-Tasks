import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# load the data from csv file to Pandas DataFrame
df = pd.read_csv('train.csv')

df.head()

df.shape

df.describe()

df.isnull()

df.isnull().sum()

df['Age'].fillna(df['Age'].mean(), inplace=True)

df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

df['Embarked'].isnull().sum()

df['Age'].isnull().sum()

df=df.drop(columns='Cabin', axis=1)

df

df['family_size'] = df['SibSp'] + df['Parch'] + 1
print(df[['SibSp', 'Parch', 'family_size']].head())

df.replace({'Sex':{'male':0, 'female':1}, 'Embarked':{'S':0, 'C':1, 'Q':2}}, inplace=True)

df.head()

X=df.drop(columns=['PassengerId','Name','Ticket','Survived'],axis=1)
Y=df['Survived']

Y

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=2)

X_train.isnull().sum()

"""***Logistic Regression***"""

model=LogisticRegression()

model.fit(X_train,Y_train)

X_train_p=model.predict(X_train)

X_train_p

training_data_accuracy=accuracy_score(Y_train,X_train_p)
training_data_accuracy

X_test_p = model.predict(X_test)
X_test_p

testing_data_accuracy=accuracy_score(Y_test,X_test_p)
testing_data_accuracy

"""***Decision Tree***"""

tree = DecisionTreeClassifier()

tree.fit(X_train, Y_train)

X_train_p_tree = tree.predict(X_train)

training_data_accuracy_tree = accuracy_score(Y_train, X_train_p_tree)
training_data_accuracy_tree

X_test_p_tree = tree.predict(X_test)

testing_data_accuracy_tree = accuracy_score(Y_test, X_test_p_tree)
testing_data_accuracy_tree

"""***Random Forest***"""

randomf=RandomForestClassifier()

randomf.fit(X_train,Y_train)

X_train_p_rf = randomf.predict(X_train)

training_data_accuracy_rf = accuracy_score(Y_train, X_train_p_rf)
training_data_accuracy_rf

X_test_p_rf = randomf.predict(X_test)

testing_data_accuracy=accuracy_score(Y_test,X_test_p_rf)
testing_data_accuracy

"""***Optimized and Hyperperameter Tuning of Decesion Tree***"""

from sklearn.model_selection import GridSearchCV
model_tree = DecisionTreeClassifier(random_state=42)

param_grid = {
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 10, 20],
    'min_samples_leaf': [1, 5, 10],
    'max_leaf_nodes': [None, 10, 20, 50]
}


grid_search = GridSearchCV(estimator=model_tree, param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')
grid_search.fit(X_train, Y_train)

best_params = grid_search.best_params_
print("Best Parameters:", best_params)


best_model_tree = DecisionTreeClassifier(**best_params)
best_model_tree.fit(X_train, Y_train)

# Training accuracy
X_train_p_tree = best_model_tree.predict(X_train)
training_data_accuracy_tree = accuracy_score(Y_train, X_train_p_tree)
print("Optimized Decision Tree Training Data Accuracy:", training_data_accuracy_tree)

# Testing accuracy
X_test_p_tree = best_model_tree.predict(X_test)
testing_data_accuracy_tree = accuracy_score(Y_test, X_test_p_tree)
print("Optimized Decision Tree Testing Data Accuracy:", testing_data_accuracy_tree)

"""***As a result the best model is Random Forest.***"""
