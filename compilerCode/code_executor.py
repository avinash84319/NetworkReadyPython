"""
This module is responsible for executing the code in different modes.
"""


import json
import requests
import concurrent.futures


def seq_code_execute(r):
    """
    This function will execute the code and return the $variables.
    input: r (redis),reads the code from seq_code.py
    output: None, variables saved in redis
    """

    # executing the code
    exec("".join(open('seq_cd/seq_code.py').read()),{})

    return None

def server_par_code_executor(hosts,path_to_req):
    """
    This function will execute the parallel user code.
    input:hosts list of strings, reads the code from par_code.py
          path_to_req: string: path to requirements.txt
    output:None, output at the desired location
    """

    # executing the code on hosts concurrently by sending the par files to the hosts
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(requests.post,f"{host}/execute",files={'code_file':open(f'par_cd/par_code_{i}.py','rb'),'req_file':open(path_to_req,'rb')}) for i,host in enumerate(hosts)]
        for f in concurrent.futures.as_completed(results):
            if f.result().status_code == 200:
                print(f"Code executed successfully at {f.result().url}")
            else:
                # stop the execution if error occured
                print(f"Error occured at {f.result().url}")
                exit()
                

    return None