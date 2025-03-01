# ColumnTransformer -Applies different transformations to specific columns of a dataset
                    # -Returns a transformed DataFrame/array with modified features
# Pipeline -  Works on end-to-end data processing
#          - Returns a complete workflow, including transformation + model

# REAL DIFFERENCE
#pipeline tells , kya transformation lgana h, kis sequence m 
#transformer transformation lgata h  & also tells transformation kha lgana h



import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer       #SimpleImputer → Fills missing values using a specified strategy (mean, median, mode, etc.)
from sklearn.pipeline import Pipeline          #Pipeline → Combines multiple preprocessing steps into a single workflow for easy execution.
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.util import save_object #related to saving back to pickle file

@dataclass
class DataTransformationConfig:                          #we are using picke file to store blueprint 
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")  #This contains  data transformation steps
                                                          #it does not create file or folder, just returns path

class DataTransformation:           #This class returns a transformation blueprint
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data trnasformation
        
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
                                       #[ Square brackets → Used for lists,
            num_pipeline= Pipeline(    #( Parentheses → Used for function calls  , here Pipeline is a function
                steps=[                
                ("imputer",SimpleImputer(strategy="median")), #median kyo ki data m outliers h
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False)) #with_mean=False is used because one-hot data has many zeros,
                ]                                        # and subtracting the mean can mess it up and use more memory
                                                          #. This way, scaling happens properly without causing issues
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor    #This preprocessor object will be used later to transform raw data
        
        except Exception as e:
            raise CustomException(e,sys)
        


#we are calling this fuction in data ingestion so we have imported this file in ingestion
#wha p apan ye function call krenge with arguments                      #IMPORTANT IMPORTANT IMPORTANT
#fn call k baad , yha se data leke wapas whi jayenge
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)  #these paths are coming from data ingestion thru parameters
            test_df=pd.read_csv(test_path)    #now we have train & test dataframe

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()  #yha apan blueprint ko dusra naam de rhe h

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]
                                                                    #these are final dataframe before transformation
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)  
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)  #actual transformation
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            #matlab apan ne jo  phle split kiya tha x & y m  , ab usi ko wapas jod rhe 
            # #np.c_[] is used to concatenate arrays column-wise. It stacks arrays side by side
              
            train_arr = np.c_[        
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

                                        #in save_object we are giving kya store krna h aur kha krna h
            save_object(                #used for saving pickle file  #we are using picke file to store blueprint 

                file_path=self.data_transformation_config.preprocessor_obj_file_path, #This is file path for saving the preprocessor
                obj=preprocessing_obj     # obj is the actual blueprint               # object (like a transformation pipeline,

            )

            return (
                train_arr,                                                  #transformed training data.
                test_arr,                                                   #ransformed test data.
                self.data_transformation_config.preprocessor_obj_file_path, # File path where blueprint is saved.
            )
        except Exception as e:
            raise CustomException(e,sys)
