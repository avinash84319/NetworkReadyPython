"""
this module will contain the code verifier functions
"""

import json

def verify_dollar_variables(r,variables):

    """
    This function will verify if all the $variables are lists after sequential code execution
    input: r (redis),variables (list of strings)
    output: None, raises exception if the variables are not lists
    """ 

    for variable in variables:
        
        variable_value = r.get(variable[1:])
        variable_value = json.loads(variable_value)

        if not isinstance(variable_value,list):
            raise Exception("The variable "+variable+" is not a list")

    return None

