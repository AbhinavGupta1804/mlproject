import sys
import pandas as pd
import os
from src.exception import CustomException
from src.util import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")                #phle path bnayenge
            preprocessor_path=os.path.join('artifacts','proprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)                   #fir model and transformation ko taiyaar krenge
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)                #actual transformation
            preds=model.predict(data_scaled) #this .predict fn is coming from pickle file      #actual prediction
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)


#this class will be responsible in mapping all inputs that we are giving in the html to 
#backend with this particular values & returning data in form of dataframe so that model can process it 
class CustomData:                     
    def __init__(  self,        
        gender: str,                # custom data  passes data from user to model
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,         #it is not necessary to provide datatype
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {      
                "gender": [self.gender],             #Without [], it would cause an error because pandas 
                "race_ethnicity": [self.race_ethnicity],             #expects lists (or other iterables).
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)   #It converts the dictionary into a pandas DataFrame so the model can process the user input.

        except Exception as e:
            raise CustomException(e, sys)

