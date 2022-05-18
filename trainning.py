# -*- coding: utf-8 -*-
"""
Created on Wed May 18 09:37:50 2022

@author: ngomi
"""
# In[0]: IMPORT AND SETTINGS
import pandas as pd
import numpy as np
from statistics import mean

import joblib # new lib
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

# In[3]: Trainning data
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

new_training = True
clf = None
if new_training:
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    clf.fit(train_set, train_set_labels)
    store_model(clf, model_name = "SVC")      
else:
    clf = load_model("SVC")

print(test_set_labels)
print(clf.predict(test_set))

# In[4]: Validation
from sklearn.model_selection import cross_val_score
print('\n____________ K-fold cross validation ____________')

run_evaluation = True
if run_evaluation:
    from sklearn.model_selection import KFold
    cv = KFold(n_splits=5,shuffle=True,random_state=37) # cv data generator: just a try to persist data splits (hopefully)

    model_name = "SVC" 
    nmse_scores = cross_val_score(clf, train_set, train_set_labels, cv=3, scoring='neg_mean_squared_error')
    rmse_scores = np.sqrt(nmse_scores)
    joblib.dump(rmse_scores,'saved_objects/' + model_name + '_rmse.pkl')    
    print("SVC rmse: ", rmse_scores.round(decimals=1))
    print("Avg. rmse: ", mean(rmse_scores.round(decimals=1)),'\n')
else:
    # Load rmse
    model_name = "SVC" 
    rmse_scores = joblib.load('saved_objects/' + model_name + '_rmse.pkl')
    print("\SVC rmse: ", rmse_scores.round(decimals=1))
    print("Avg. rmse: ", mean(rmse_scores.round(decimals=1)),'\n')



