"""
this module will contain the code verifier functions
"""

from compilerCode import data_serializer

import numpy as np
import pandas as pd

def verify_dollar_variables(r,variables):

    """
    This function will verify if all the $variables are lists,numpy arrays or pandas dataframes
    input: r (redis),variables (list of strings)
    output: None, raises exception if the variables are not lists
    """ 

    for variable in variables:
        
        variable_value = r.get(variable[2:])
        variable_value = data_serializer.deserialize_data(variable_value)

        if type(variable_value) not in [list,np.ndarray,pd.DataFrame]:
            print(f"Variable {variable} is not a list,numpy array or pandas dataframe")
            exit()

    return None

