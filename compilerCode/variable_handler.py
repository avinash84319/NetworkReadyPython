""" Code for all variable handling in the program. """

import json

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


def divide_variables_in_redis_no_of_hosts(r,variables,no_of_hosts):
    """
    This function will divide the variables in the given list into the no of hosts given.
    input:r (redis),variables (list of variables), no_of_hosts (int)
    output: None, variables saved in redis
    """
    
    for variable in variables:
        
        variable_value = r.get(variable[1:])
        variable_value = json.loads(variable_value)
        
        # dividing the variable into the no of hosts using generator
        # here based on different strategies the variable can be divided (next version)
        variable_value = divide_list(variable_value,no_of_hosts)
        
        # saving the variable in redis
        for i,variable_part in enumerate(variable_value):
            r.set(f"{variable[1:]}${i}",json.dumps(variable_part))

    return None

def merge_variables_in_redis_no_of_hosts(r,variables,no_of_hosts):
    """
    This function will merge the variables in the given list into the no of hosts given.
    input:r (redis),dollor variables (list of variables), no_of_hosts (int)
    output: None, variables printed on terminal
    """
    
    for variable in variables:
        
        variable_value = []
        
        # merging the variable from the no of hosts
        for i in range(no_of_hosts):
            variable_part = r.get(f"{variable[1:]}${i}")
            variable_part = json.loads(variable_part)
            variable_value.extend(variable_part)

        print(f"value of {variable} after par execution: {variable_value[:10]} ... ")

        # saving the variable in redis
        r.set(variable[1:],json.dumps(variable_value))

    return None