""" Code for all variable handling in the program. """

from compilerCode import data_serializer

import numpy as np
import pandas as pd

def divide_list(l, n):
    """
    This function will divide the given list into n parts.
    input: l (list), n (int)
    output: list of n lists
    """

    # calculating the length of each part
    length = len(l) // n 

    # dividing the list into n parts
    for i in range(0, len(l), length):

        # if no of parts is equal to no of hosts put remaining elements in the last part
        if i>= n*length-1:
            yield l[i:]
            break

        else:
            yield l[i:i + length]

def divide_numpy_array(a, n):
    """
    This function will divide the given numpy array into n parts.
    input: a (numpy array), n (int)
    output: list of n numpy arrays
    """

    # calculating the length of each part
    length = a.shape[0] // n 

    # dividing the numpy array into n parts
    for i in range(0, a.shape[0], length):

        # if no of parts is equal to no of hosts put remaining elements in the last part
        if i>= n*length-1:
            yield a[i:]
            break

        else:
            yield a[i:i + length]

def divide_dataframe(df, n):
    """
    This function will divide the given pandas dataframe into n parts.
    input: df (pandas dataframe), n (int)
    output: list of n pandas dataframes
    """

    # calculating the length of each part
    length = df.shape[0] // n 

    # dividing the dataframe into n parts
    for i in range(0, df.shape[0], length):

        # if no of parts is equal to no of hosts put remaining elements in the last part
        if i>= n*length-1:
            yield df.iloc[i:]
            break

        else:
            yield df.iloc[i:i + length]


def divide_variables_in_redis_no_of_hosts(r,variables,no_of_hosts):
    """
    This function will divide the variables in the given list into the no of hosts given.
    input:r (redis),variables (list of variables), no_of_hosts (int)
    output: type of variable_value, and saves divided variables in redis
    """
    
    for variable in variables:
        
        variable_value = r.get(variable[2:])
        variable_value = data_serializer.deserialize_data(variable_value)
        
        # dividing the variable into the no of hosts using generator
        # here based on different strategies the variable can be divided (next version)

        var_type=type(variable_value)

        #check type of variable_value
        if type(variable_value) == list:
            variable_value = divide_list(variable_value,no_of_hosts)
        
        if type(variable_value) == np.ndarray:
            variable_value = divide_numpy_array(variable_value,no_of_hosts)

        if type(variable_value) == pd.DataFrame:
            variable_value = divide_dataframe(variable_value,no_of_hosts)
        
        # saving the variable in redis
        for i,variable_part in enumerate(variable_value):
            r.set(f"{variable[2:]}${i}",data_serializer.serialize_data(variable_part))

    return var_type

def merge_variables_in_redis_no_of_hosts(r,variables,no_of_hosts,var_type):
    """
    This function will merge the variables in the given list into the no of hosts given.
    input:r (redis),dollor variables (list of variables), no_of_hosts (int) ,var_type (type of variable)
    output: None, variables printed on terminal
    """

    print(f'var type is {var_type}')

    if var_type == list:
        merge_list_variables_in_redis_no_of_hosts(r,variables,no_of_hosts)

    if var_type == np.ndarray:
        merge_numpy_array_variables_in_redis_no_of_hosts(r,variables,no_of_hosts)

    if var_type == pd.DataFrame:
        merge_dataframe_variables_in_redis_no_of_hosts(r,variables,no_of_hosts)

    return None

def merge_list_variables_in_redis_no_of_hosts(r,variables,no_of_hosts):
    """
    This function will merge the list variables in the given list into the no of hosts given.
    input:r (redis),dollor variables (list of variables), no_of_hosts (int)
    output: None, variables printed on terminal
    """

    for variable in variables:
        
        variable_value = []
        
        # merging the variable from the no of hosts
        for i in range(no_of_hosts):
            variable_part = r.get(f"{variable[2:]}${i}")
            variable_part = data_serializer.deserialize_data(variable_part)

            if variable_part==None:
                print(f"variable {variable[2:]}${i} is None")
                continue
            else:
                variable_value.extend(variable_part)

        print(f"value of {variable} after par execution: {variable_value[:10]} ... ")

        # saving the variable in redis
        r.set(variable[2:],data_serializer.serialize_data(variable_value))

    return None

def merge_numpy_array_variables_in_redis_no_of_hosts(r,variables,no_of_hosts):
    """
    This function will merge the numpy array variables in the given list into the no of hosts given.
    input:r (redis),dollor variables (list of variables), no_of_hosts (int)
    output: None, variables printed on terminal
    """

    for variable in variables:
        
        variable_value = np.array([])

        # merging the variable from the no of hosts
        for i in range(no_of_hosts):
            variable_part = r.get(f"{variable[2:]}${i}")
            variable_part = data_serializer.deserialize_data(variable_part)
            variable_value = np.append(variable_value,variable_part)

        # saving the variable in redis
        r.set(variable[2:],data_serializer.serialize_data(variable_value))

        print(f"value of {variable} after par execution: {variable_value[:10]} ... ")

    return None

def merge_dataframe_variables_in_redis_no_of_hosts(r,variables,no_of_hosts):
    """
    This function will merge the dataframe variables in the given list into the no of hosts given.
    input:r (redis),dollor variables (list of variables), no_of_hosts (int)
    output: None, variables printed on terminal
    """

    for variable in variables:
        
        variable_value = pd.DataFrame()

        # merging the variable from the no of hosts
        for i in range(no_of_hosts):
            variable_part = r.get(f"{variable[2:]}${i}")
            variable_part = data_serializer.deserialize_data(variable_part)
            variable_value = pd.concat([variable_value,variable_part])
        
        # saving the variable in redis
        r.set(variable[2:],data_serializer.serialize_data(variable_value))

        print(f"value of {variable} after par execution: {variable_value.head()} ... ")

    return None