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
        f_object.close()

clf = load_model("SVC")


# In[1]: Start API
from flask import Flask
from flask import request
from datetime import datetime

app = Flask(__name__)

@app.route("/student/<id>", methods = ['POST'])
def postExamData(id):
    jsonData = request.get_json()
    data = jsonData.get('data')
    result = clf.predict([data])
    print(result[0])
    result = result.tolist()
    result.extend(data)
    result.append(id)
    result.append(datetime.now())
    result.append(request.remote_addr)
    insertData(result)
    return result[0]

app.run()