"""
This module is responsible for executing the code in different modes.
"""
from compilerCode import workspace_manager

import os
import json
import concurrent.futures
from dotenv import load_dotenv

from compilerCode import communication

load_dotenv()

workspace_data_path=os.getenv("COMPILER_WORKSPACE_PATH")

def seq_code_execute(r):
    """
    This function will execute the code and return the $variables.
    input: r (redis),reads the code from seq_code.py
    output: None, variables saved in redis
    """

    # executing the code
    exec("".join(open(workspace_data_path+"/"+'seq_cd/seq_code.py').read()),{})

    return None

def server_par_code_executor(hosts,path_to_req,r,server_workspace_ids):
    """
    This function will execute the parallel user code.
    input:hosts list of strings, reads the code from par_code.py
          path_to_req: string: path to requirements.txt
          r: redis
         server_workspace_ids: list of strings: ids of the server workspaces
    output:None, output at the desired location
    """

    # setup environment for the code execution
    workspace_manager.setup_environment(hosts,path_to_req,server_workspace_ids)

    # executing the code on hosts concurrently by sending the par files to the hosts
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(communication.post,f"{host}/execute",json={'code_file':open(workspace_data_path+f'par_cd/par_code_{i}.py').read(),"server_workspace_id":server_workspace_ids[host]}) for i,host in enumerate(hosts)]
        
        # checking the results
        for f in concurrent.futures.as_completed(results):
            try:
                response = f.result()
                if response.status_code == 200:
                    print(f"Code executed successfully at {response.url}")
                elif response.status_code == 500:
                    print(f"Error occurred at {response.url} error: {response.json()['error']}")
                    raise Exception(f"Error occurred at {response.url} error: {response.json()['error']}")
                else:
                    # Handle HTTP errors
                    response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error occurred: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error occurred while connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout occurred: {errt}")
            # except requests.exceptions.RequestException as err:
            #     print(f"An error occurred: {err}")

    completed_hosts=[]
    #check all hosts who have executed code properly
    for no,host in enumerate(hosts):
        if r.get(f"flag_for_host_execution_{no}") ==b'2':
            completed_hosts.append(host)
    
    # check if any code failed to execute and execute in other servers
    for no,host in enumerate(hosts):
        
        if r.get(f"flag_for_host_execution_{no}") !=b'2':

            for new_host in hosts:
                if new_host in completed_hosts:
                    print(f"Trying second pass for {host}'s code in {new_host}") 
                    # send the code to the new host
                    try:
                        communication.post(f"{new_host}/execute",json={'code_file':open(workspace_data_path+f'par_cd/par_code_{no}.py').read(),"server_workspace_id":server_workspace_ids[host]})
                    except requests.exceptions.HTTPError as errh:
                        print(f"HTTP Error occurred: {errh} at {new_host}")
                    except requests.exceptions.ConnectionError as errc:
                        print(f"Error occurred while connecting: {errc} at {new_host}")
                    except requests.exceptions.Timeout as errt:
                        print(f"Timeout occurred: {errt} at {new_host}")
                    except requests.exceptions.RequestException as err:
                        print(f"An error occurred: {err} at {new_host}")
                    # check if the code executed properly
                    if r.get(f"flag_for_host_execution_{no}") ==b'2':
                        print(f"Code executed successfully at {new_host}")
                        completed_hosts.append(host)
                        break
                    else:
                        print(f"Error occured at {new_host} also so exiting something wrong in code of par_cd/par_code_{no}")
                        exit()

                

    return None


def wait_for_all_hosts_to_complete(r,no_of_hosts):
    """
    This function will wait for all hosts to complete the execution.
    input: r (redis), no_of_hosts (int): number of hosts
    output: None, waits for all hosts to complete
    """

    # wait for all hosts to complete the execution
    while True:
        if all([r.get(f"flag_for_host_execution_{i}") ==b'2' for i in range(no_of_hosts)]):
            print("All hosts have completed the execution")
            break
        print("Waiting for all hosts to complete the execution")

    return None