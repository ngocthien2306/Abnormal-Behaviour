# -*- coding: utf-8 -*-
"""
Created on Wed May 18 09:37:50 2022

@author: ngomi
"""
# In[0]: IMPORT AND SETTINGS
import pandas as pd
from camera import Camera 

import numpy as np
from statistics import mean
import joblib


def store_model(model, model_name = ""):
    # NOTE: sklearn.joblib faster than pickle of Python
    # INFO: can store only ONE object in a file
    if model_name == "": 
        model_name = type(model).__name__
    joblib.dump(model,'models/' + model_name + '_model.pkl')
def load_model(model_name):
    # Load objects into memory
    #del model
    model = joblib.load('models/' + model_name + '_model.pkl')
    #print(model)
    return model

raw_data = pd.read_csv('trainning_data.csv')

# In[1]: DISCOVER THE DATA
print('\n____________ Dataset info ______________________________')
dataInfo = raw_data.info()
print(dataInfo)      
print('\n____________ Some first data examples __________________')
dataHead = raw_data.head(3)
print(dataHead) 
print('\n____________ Counts on a feature _______________________')
dataCount = raw_data['label'].value_counts()
print(dataCount) 
print('\n____________ Statistics of numeric features ____________')
dataDescribe = raw_data.describe()
print(dataDescribe)    

# In[2]: Prepare data
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(raw_data, test_size=0.2, random_state=42) # set random_state to get the same training set all the time, 

train_set_labels = train_set["label"].copy()
train_set = train_set.drop(columns = "label") 
test_set_labels = test_set["label"].copy()
test_set = test_set.drop(columns = "label") 

# In[3]: Fine turnning
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold   
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

new_tuning = False

grid_search = None
C = 0
gamma = ''
kernel = ''
if new_tuning:
    cv = KFold(n_splits=5,shuffle=True,random_state=37)
    model = SVC()
    param_grid = [
        # Try 3
        {
         'kernel':['rbf'],
         'C': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 
         'gamma': ['scale']
        },

    ];
    grid_search = GridSearchCV(model, param_grid, cv=cv)
    grid_search.fit(train_set, train_set_labels)
    joblib.dump(grid_search,'saved_objects/SVC_gridsearch.pkl')
    (c, gamma, kernel) = grid_search.best_params_
    print(grid_search.best_params_)
    print(grid_search.best_score_)  
    print(grid_search.best_estimator_.C)
    C       = grid_search.best_estimator_.C
    gamma   = grid_search.best_estimator_.gamma
    kernel  = grid_search.best_estimator_.kernel
else:
    grid_search = joblib.load('saved_objects/SVC_gridsearch.pkl')
    C       = grid_search.best_estimator_.C
    gamma   = grid_search.best_estimator_.gamma
    kernel  = grid_search.best_estimator_.kernel

# Try 1
"""
{
 'kernel':['rbf'],
 'C': [0.1, 10, 50, 100], 
 'gamma': ['scale', 'auto']
},
"""
# Try 2
"""
{
 'kernel':['poly'],
 'C': [0.1, 10, 50], 
 'degree': [3, 10, 20], 
 'gamma': ['scale', 'auto'],
 'coef0': [1, 5, 10], 
},
"""
# Try 3
"""
{
 'kernel':['rbf'],
 'C': [5, 8, 10, 20, 30], 
 'gamma': ['scale']
},
"""
# Try 4
"""
{
 'kernel':['rbf'],
 'C': [1, 2, 3, 4, 5], 
 'gamma': ['scale']
},
"""
# Try 4
"""
{
 'kernel':['rbf'],
 'C': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 
 'gamma': ['scale']
},
"""

# In[4]: Trainning data
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

new_training = False
clf = None
if new_training:
    clf = make_pipeline(SVC(C=C,kernel=kernel, gamma=gamma))
    clf.fit(train_set, train_set_labels)
    store_model(clf, model_name = "SVC")      
else:
    clf = load_model("SVC")

print(test_set_labels)
print(clf.predict(test_set))
print('Score:')
print(clf.score(test_set, test_set_labels))


