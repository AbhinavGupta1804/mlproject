#How it Works:
# 1️⃣ User submits data via an HTML form.
# 2️⃣ Flask receives the data and converts it into a DataFrame.
# 3️⃣ Flask loads the trained model (from model.pkl) and the preprocessor (preprocessor.pkl).
# 4️⃣ Data is transformed using the preprocessor.
# 5️⃣ Model predicts the result based on the transformed data.
# 6️⃣ Flask returns the prediction to the frontend (HTML page).

# 👉 The Flask file is responsible for calling the model and handling user requests, but the model itself is stored and trained separately.



#GET request = You ask for a menu 📜 (just fetching data, no changes).
#POST request = You place an order 🍕 (sending new data to be processed).

from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application                 

## Route for a home page
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:                                     #POST request
        data=CustomData(   #this function is written in predict_pipeline #it passes data from user to model
            gender=request.form.get('gender'),                           ##here we are inputing data from html form
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        pred_df=data.get_data_as_data_frame() #it converts above user data into dataframe 
        print(pred_df)                        ##this function is present in predict_pipeline inside customdata
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)           #will return the predicted math score
        print("after Prediction")
        return render_template('home.html',results=results[0])
                                   #Using results[0] extracts the first (and only) value from this list/array, so we 
                                   # return just the predicted math score instead of a list.
    

if __name__=="__main__":
    app.run(debug=True)        

