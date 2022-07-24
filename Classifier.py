from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression as lr
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from trainning import store_model

class Classifiers(object):

    def __init__(self,train_data,train_labels,name,hyperTune=True):
        self.train_data=train_data
        self.train_labels=train_labels
        self.model_name=name
        self.set_model_name()
        #self.construct_all_models(hyperTune)
        self.accuracy = ""
        self.info_train = ""
        self.test_core = ""

    def return_info(self):
        return self.info_train
    
    def return_accuracy(self):
        return self.accuracy
    
    def return_test_core(self):
        return self.test_core
    
    def set_model_name(self):
        model = ""
        if self.model_name == "Suport Vector Machine":
            model = "SVM"
    
        elif  self.model_name == "Logistic Regression":
            model = "LogisticRegression"
            
        elif  self.model_name == "KNeighbors Classifier":
            model = "KNN"
            
        elif self.model_name == "Random Forest Classifier":
            model = "RandomForestClassifier"
            
        self.model_name = model
        
        
    def store_model(self, model, model_name = ""):
        # NOTE: sklearn.joblib faster than pickle of Python
        # INFO: can store only ONE object in a file
        if model_name == "": 
            model_name = type(model).__name__
        joblib.dump(model,'models/' + model_name + '_model.pkl')
    
    def construct_all_models(self,hyperTune):
        if hyperTune:
            #3 models KNN SCM and LR
            self.models={'SVM':[SVC(kernel='linear',probability=True),dict(C=np.arange(0.01, 2.01, 0.2))],\
                         'LogisticRegression':[lr(),dict(C=np.arange(0.1,3,0.1))],\
                         'KNN':[KNeighborsClassifier(),dict(n_neighbors=range(1, 100))],\
                         'RandomForestClassifier': [RandomForestClassifier(n_estimators=100), dict(min_samples_leaf=np.arange(2, 20, 1))]}
            for name,candidate_hyperParam in self.models.items():
                #update each classifier after training and tuning
                if name == self.model_name:
             
                    self.models[name] = self.train_with_hyperParamTuning(candidate_hyperParam[0],name,candidate_hyperParam[1])
                   
            print ('\nTraining process finished\n\n\n')
            
        return self.accuracy, self.test_core, self.info_train

    def train_with_hyperParamTuning(self,model,name,param_grid):
        #grid search method for hyper-parameter tuning
        grid = GridSearchCV(model, param_grid, cv=10, scoring='accuracy', n_jobs=-1)
        grid.fit(self.train_data, self.train_labels)
        joblib.dump(grid,'saved_objects/' + name  + '_gridsearch.pkl')
        self.store_model(grid, name)
        
        self.info_train = '\nThe best hyper-parameter for -- {} is {}, the corresponding mean accuracy through 10 Fold test is {} \n'\
            .format(name, grid.best_params_, grid.best_score_)
        print(self.info_train)

        model = grid.best_estimator_
        train_pred = model.predict(self.train_data)
        self.accuracy = '{} train accuracy = {}\n'.format(name,(train_pred == self.train_labels).mean())
        print(self.accuracy)
        
       
        return model

    def prediction_metrics(self,test_data,test_labels,name):

        #accuracy
        self.test_core = '{} test accuracy = {}\n'.format(self.model_name,(self.models[self.model_name].predict(test_data) == test_labels).mean())
        print(self.test_core)

        #AUC of ROC
        prob = self.models[self.model_name].predict_proba(test_data)
        auc=roc_auc_score(test_labels,prob[:,1])
        print('Classifier {} area under curve of ROC is {}\n'.format(self.model_name,auc))

        #ROC
        fpr, tpr, thresholds = roc_curve(test_labels, prob[:,1], pos_label=1)
        #self.roc_plot(fpr,tpr,name,auc)
        return self.test_core

    def roc_plot(self,fpr,tpr,name,auc):
        plt.figure(figsize=(20,5))
        plt.plot(fpr,tpr)
        plt.ylim([0.0,1.0])
        plt.ylim([0.0, 1.0])
        plt.title('ROC of {}     AUC: {}\nPlease close it to continue'.format(name,auc))
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.grid(True)
        plt.show()