#common fuctionalites
                 #A pickle file saves Python OBJECTS in binary format for efficient storage and faster loading
import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
                                               
def save_object(file_path, obj):                            ## Define a function to save an object to a file
    try:
        dir_path = os.path.dirname(file_path)               ## Get the directory path from the file path

        os.makedirs(dir_path, exist_ok=True) ## Create the directory if it doesn't exist (without raising an error)

        with open(file_path, "wb") as file_obj:   # Open the file at 'file_path' in write-binary mode
            pickle.dump(obj, file_obj)          #This takes the object obj and saves it into the file in binary form.

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}   #we will be returning this after storing model_name(not model) and r2 score 

        for i in range(len(list(models))):       #traversing in diff models
            model = list(models.values())[i]   #bcoz values contain fuctions of algorithms
            # para=param[list(models.keys())[i]]

            # gs = GridSearchCV(model,para,cv=3)
            # gs.fit(X_train,y_train)

            # model.set_params(**gs.best_params_)
            # model.fit(X_train,y_train)

            model.fit(X_train, y_train)  # Training model

            y_train_pred = model.predict(X_train)    #making predictions

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred) #calculating r2 score

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score
                   #name of model            #r2 score
        return report

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
