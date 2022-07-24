# -*- coding: utf-8 -*-
"""
Created on Wed May 18 18:32:54 2022

@author: ngomi
"""
# In[0]: Import model
from sklearn.svm import SVC
import joblib
from csv import writer

def load_model(model_name):
    # Load objects into memory
    #del model
    model = joblib.load('models/' + model_name + '_model.pkl')
    #print(model)
    return model
def insertData(row_data):
    with open('exam_data.csv', 'a', newline='') as f_object:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(row_data)  
        # Close the file object
        print("Insert successfully")
        f_object.close()

# clf = load_model("KNN")
# clf = load_model("LogisticRegression")
# clf = load_model("SVM")



def model_runing(name): 
    model = ""
    if name == "Suport Vector Machine":
        model = "SVC"
        
    elif  name == "Logistic Regression":
        model = "LogisticRegression"
        
    elif  name == "KNeighbors Classifier":
        model = "KNN"
        
    clf = load_model(model)
    
    return clf

#%%
from datetime import date
def get_date(): 
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    return d1

# In[1]: Start API
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/student/<id>", methods = ['POST'])
def postExamData(id):
    
    jsonData = request.get_json()
    data = jsonData.get('data')
    fullname = jsonData.get('fullname')
    phone = jsonData.get('phone')
    model = jsonData.get('model')
    
    clf = model_runing(model)
    result = clf.predict([data])
    print(result[0])
    
    
    result = result.tolist()
    result.extend(data)
    result.append(phone)
    result.append(fullname)
    result.append(id)
    result.append(get_date())
    result.append(request.remote_addr)
    result.append(model)
    
    print(result)
    insertData(result)
    return result[0]

app.run()