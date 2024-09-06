"""
This module is responsible for executing the code and returning the $variables.
"""


import json


def seq_code_execute(r,variables):
    """
    This function will execute the code and return the $variables.
    input: r (redis),variables(list of strings), reads the code from seq_code.py
    output: None, variables saved in redis
    """

    # executing the code
    exec("".join(open('seq_code.py').read()))

    return None

def par_code_execute(no_of_hosts):
    """
    This function will execute the parallel user code.
    input:no_of_hosts int, reads the code from par_code.py
    output:None, output at the desired location
    """

    # executing the code
    for i in range(no_of_hosts):
        exec("".join(open(f'par_cd/par_code_{i}.py').read()))

    return None