#SUMMARY
#phli class m apan ne train,test,raw data ka path define kiya
#fir apan notebook se data utha k usko 3 part m divide krke store kra diya


#all the code for reading data from anywhere
#The os module in Python provides functions to interact with the operating system, such as handling
# file paths, creating directories, reading environment variables, and executing system commands.

#train_data_path: str=os.path.join('artifacts',"train.csv") #: is used for datatype hinting 
#train_data_path is a string that stores the path to "train.csv" inside the "artifacts" #artifacts/train.csv
#This line SETS THE PATH where the training data (train.csv) will be saved or accessed, ensuring organized storage within the "artifacts" directory.

#header=True → Ensures that column names are included in the CSV
#index=False ka matlab hai ki CSV file mein pandas dataframe ka index column save nahi hoga. example =0,1,2,3,4....
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# from src.components.data_transformation import DataTransformation
# from src.components.data_transformation import DataTransformationConfig

# from src.components.model_trainer import ModelTrainerConfig
# from src.components.model_trainer import ModelTrainer
@dataclass #if we dont write it , then we will have to define __init__ function like in dataingestion class
#CLASS DATAINGESTIONCONFIG DEFINES FILE PATHS FOR STORING OR ACCESSING TRAIN, TEST, 
# AND RAW DATA DURING THE DATA INGESTION PROCESS
#means this only stores path to file
class DataIngestionConfig: #any input that is required in my data ingestion , that will pass thru this dataingestionconfig 
    train_data_path: str =os.path.join('artifacts',"train.csv")  #artifacts/train.csv
    test_data_path: str =os.path.join('artifacts',"test.csv")  #they provides the file paths for reading or storing train,.
    raw_data_path: str =os.path.join('artifacts',"data.csv")  # test, and raw data during the ingestion process


#if you have some other functions inside class then we should not use dataclass
#agar init m self nhi lgagyege to init ka data/variables niche wale funtion use ni kr payenge
class DataIngestion:
    def __init__(self):#Agar self hata diya, toh class ke andar jo data store ho raha hai, usko access nahi kar paoge.
        self.ingestion_config=DataIngestionConfig()  #this ingestionn config has 3 variables data from above

    def initiate_data_ingestion(self):  #to read data from database
        logging.info("Entered the data ingestion method or component") 
        try:
            df=pd.read_csv('notebook\data\stud.csv')      
            logging.info('Read the dataset as dataframe')    #add this whereever error can occur

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #If the directory doesn’t exist, os.makedirs() will create it. 
                                                                                             #If it already exists, the exist_ok=True argument prevents errors.
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)   #This line saves the entire dataset (df) as a CSV file at the location
                                                                                     # specified by self.ingestion_config.raw_data_path, which is defined as artifacts/data.csv
            #abhi apan ne notebook se data uthaya # Us data ko artifacts/data.csv me store kar diya  
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path, #returns path where train data is stored
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__": #It makes sure the code inside this runs only when you run this file directly, not when you import it somewhere else.
    obj=DataIngestion()                                  #initialising object
    train_data,test_data=obj.initiate_data_ingestion()   #storing path of train and test data

    # data_transformation=DataTransformation()
    # train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    # modeltrainer=ModelTrainer()
    # print(modeltrainer.initiate_model_trainer(train_arr,test_arr))






