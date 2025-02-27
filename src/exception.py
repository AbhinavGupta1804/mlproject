#This custom exception class does not handle a specific type of error—instead, 
# it acts as a universal error handler. It captures all exceptions and provides
# detailed error messages for debugging.

#any exception that is basically getting controlled , SYS library will automatically
#have that information.


# ABOUT FUNCTION - error_message_detail
#AIM - whenever  there is an exception , i want to push my own custom message

#Function Purpose
#This function extracts detailed information about an exception, including:
#✔ File name where the error occurred
#✔ Line number where the error happened
#✔ Error message
#It helps in debugging by providing useful context about the error.


import sys
import logging
from src.logger import logging
                         #error - whatever msg i am getting about error 
def error_message_detail(error,error_detail:sys): #other parameter will be  my error detail and it will be present inside SYS
    _,_,exc_tb=error_detail.exc_info()            # sys.exc_info() returns a tuple (exception_type, exception_value, traceback)
                                                  # We only need the third value (traceback object), so we use _ for the first two.
                                                  #all imp info gets stored in exc_tb
    file_name=exc_tb.tb_frame.f_code.co_filename      #will give file name in which exception is there
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))  #this error is provided in parameters

    return error_message
#all the shit like .tb_frame.f_code => you will get this in documentation , no need to remember    




#Custom exception class to generate detailed error messages.
#so whenever i raise custom excdption ,first of all it is inheriting the parent exception,
#whatever error message is basically coming from above function , that particular
#  error message will come over here and we will initialize it to error_message

class CustomException(Exception):   # niche we are Inheriting from this Exception using super        
    def __init__(self,error_message,error_detail:sys):  #this fuction is automatically called when custom exception is raised
                                         #error_message → The actual error message (e.g., "division by zero").
        super().__init__(error_message)  # calls the constructor of the parent class (Exception) and passes error_message to it.  This allows CustomException to behave like a normal exception when raised.
        self.error_message=error_message_detail(error_message,error_detail=error_detail) #full message is stored in self.error_message
        #self is a reference to the current instance of the class. It allows a class to access its own attributes and methods
    
    def __str__(self):             #to print error message
        return self.error_message
    
# if __name__ == "__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("divide by zero")
#         raise CustomException(e,sys)        
    

#- error_message (str): The actual exception message.
#- error_detail (sys): The sys module for accessing traceback details




#1
# try:
#     x = 1 / 0  # ❌ Oops! This causes a ZeroDivisionError
# except Exception as e:
#     raise CustomException(e, sys)  # 🚀 Calls CustomException


#2
#Python automatically calls the __init__ method of CustomException.
#raise CustomException(e, sys)
#👉 This calls __init__ in CustomException, passing e (the error) and sys


#3
# def __init__(self, error_message, error_detail: sys):
# 👉 error_message holds "division by zero".
# 👉 error_detail is sys, which helps track the error’s file name and line number

#4
# super().__init__(error_message)
# 👉 This calls Exception's __init__() method and passes error_message to it.
#  This allows CustomException to behave like a normal exception when raised.

#5
#self.error_message = error_message_detail(error_message, error_detail=error_detail)
#This line calls a function to generate a detailed error message and then stores it 
# inside the self.error_message variable.

