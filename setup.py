from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:   
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj: #creating this requirement file as temporary object
        requirements=file_obj.readlines() #to read lines in txt file
        requirements=[req.replace("\n","") for req in requirements] #replacing /n on end of every line in txt file with nospace

        if HYPEN_E_DOT in requirements:   #to remove -e .
            requirements.remove(HYPEN_E_DOT)   #bcoz we dont want -e . here, which is used to
                                               # simultaneouly install requirements.txt file and 
    return requirements                        #also run setup.py file to build the packages , 
                                         # -e . in txt file will automatically trigger setup.py file 

setup(
name='mlproject',
version='0.0.1',
author='abhinav',
author_email='abhi1804gupta@gmail.com',

packages=find_packages(), #when this is running it will go and  see how many folders 
                         #have this __init__.py , and will directly consider that 
                         # folder(src in our case) as a package.

install_requires=get_requirements('requirements.txt')      #FUNCTION ABOVE 

)
#now entire project development will be happening inside the src folder
