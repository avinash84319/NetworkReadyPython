"""
This module is responsible for executing the code in different modes.
"""


import json
import requests
import concurrent.futures


def seq_code_execute(r,variables):
    """
    This function will execute the code and return the $variables.
    input: r (redis),variables(list of strings), reads the code from seq_code.py
    output: None, variables saved in redis
    """

    # executing the code
    exec("".join(open('seq_cd/seq_code.py').read()))

    return None

def par_code_execute(code):
    """
    This function will execute the parallel user code from the server.
    input:code from the server.
    output:ouput at host terminals.
    """

    exec(code)

    return None

def server_par_code_executor(hosts):
    """
    This function will execute the parallel user code.
    input:hosts list of strings, reads the code from par_code.py
    output:None, output at the desired location
    """

    # executing the code on hosts concurrently
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(requests.post,f"{host}/execute",json={"code":open(f'par_cd/par_code_{i}.py').read()}) for i,host in enumerate(hosts)]
        for f in concurrent.futures.as_completed(results):
            if f.result().status_code == 200:
                print(f"Code executed successfully at {f.result().url}")
            else:
                print(f"Error occured at {f.result().url}")

    return None