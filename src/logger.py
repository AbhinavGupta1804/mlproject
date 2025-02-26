#purpose of logger - any execution that probably happens , we should 
#be able to log all those info , execution , everything is some file
#so we will be able to track
#if there is some error , we will try to log that into a text file

import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) ## Creates a full path for the log file inside a "logs" folder
os.makedirs(logs_path,exist_ok=True) 
#it says that even though there is a file or folder , keep on appending it

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# if __name__ == "__main__":
#     logging.info("logging has started")