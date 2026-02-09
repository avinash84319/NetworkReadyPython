"""
This module will contain all the functions to handle the workspace in hosts
"""


import os
import json
import requests
from dotenv import load_dotenv

from compilerCode import communication

load_dotenv()

workspace_data_path=os.getenv("COMPILER_WORKSPACE_PATH")

def send_workspace_to_hosts(hosts,workspace_path):
    """
    This function will create the workspace for the hosts
    input: hosts (list of strings),workspace_path (string)
    output: ids (dict) host:workspace_id , creates workspace at the hosts
    """

    directory_path = workspace_path.split("/")[-1]
    workspace_path = "/".join(workspace_path.split("/")[:-1])

    workspace_json = get_workspace_json(workspace_path,directory_path)

    ids={}

    for no,host in enumerate(hosts):
        try:
            response = communication.post(f"{host}/workspace",json=workspace_json)
            if response.status_code == 200:
                print(f"Workspace created successfully at {host}")
                ids[host]=response.json()["id"]
            elif response.status_code == 500:
                print(f"Error occurred at {host} error: {response.json()['error']}")
            else:
                # Handle HTTP errors
                response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error occurred: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error occurred while connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout occurred: {errt}")

    return ids

def get_workspace_json(workspace_path,directory_path):
    """
    This function will create the workspace json file recursively
    input: workspace_path (string),directory_path (string)
    output: Json for workspace
    """

    print(workspace_path,directory_path)

    ignore_floders=['__pycache__','.git','.vscode']
    ignore_files=['.gitignore']

    workspace_json = {}
    workspace_json["path"]=directory_path

    dirs = os.listdir(workspace_path+"/"+directory_path)
    files = []
    folders = []

    for dir in dirs:
            
            if os.path.isfile(os.path.join(workspace_path,directory_path,dir)):
                files.append(dir)
            else:
                folders.append(dir)

    workspace_json["files"] = []
    workspace_json["folders"] = []

    for file in files:
        if files not in ignore_files:
            workspace_json["files"].append({"name":file,"content":open(os.path.join(workspace_path,directory_path+"/"+file)).read()})

    for folder in folders:
        if folder not in ignore_floders:
            workspace_json["folders"].append({folder:get_workspace_json(os.path.join(workspace_path),directory_path+"/"+folder)})

    return workspace_json

def server_workspace_creater(path_to_save,workspace_json):
    """
    This function will create the workspace for the servers
    input:path_to_save (string),workspace_json (dict) 
    output: None, creates workspace for servers
    """

    dirs=workspace_json["folders"]
    files=workspace_json["files"]
    directory_path = workspace_json["path"]

    if not os.path.exists(path_to_save+"/"+directory_path):
        os.makedirs(path_to_save+"/"+directory_path)
    else:
        # remove the existing files
        os.system(f"rm -rf {path_to_save}/{directory_path}/*")

    for file in files:
        with open(path_to_save+"/"+directory_path+"/"+file["name"],"w") as f:
            f.write(file["content"])

    for dir in dirs:
        for key in dir:
            server_workspace_creater(path_to_save,dir[key])

    return None


def setup_environment(hosts,path_to_req,server_workspace_ids):
    """
    This function will setup the environment for the code execution
    input: hosts (list of strings),path_to_req (string),server_workspace_ids (list of strings)
    output: None, installs the packages for the workspace
    """

    packages_installed=False

    # check if requirments already installed
    for no,host in enumerate(hosts):
        try:
            response = communication.get(f"{host}/workspace/install/check",json={"server_workspace_id":server_workspace_ids[host]})
            if response.status_code == 200:
                packages_installed=True
                print(f"Packages already installed at {host}")
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error occurred: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error occurred while connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout occurred: {errt}")


    if not packages_installed:

        for no,host in enumerate(hosts):
            try:
                response = communication.post(f"{host}/workspace/install",json={"req_file":open(path_to_req).read(),"server_workspace_id":server_workspace_ids[host]})
                if response.status_code == 200:
                    print(f"Packages installed successfully at {host}")
                elif response.status_code == 500:
                    print(f"Error occurred at {host} error: {response.json()['error']}")
                else:
                    # Handle HTTP errors
                    response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error occurred: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error occurred while connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout occurred: {errt}")

    return None

def delete_workspace_in_hosts(hosts,server_workspace_ids):

    """
    This function will delete the workspace in the hosts
    input: hosts (list of strings),server_workspace_ids (list of strings)
    output: None, deletes the workspace in the hosts
    """

    for no,host in enumerate(hosts):
        try:
            response = communication.post(f"{host}/workspace/delete",json={"server_workspace_id":server_workspace_ids[host]})
            if response.status_code == 200:
                print(f"Workspace deleted successfully at {host}")
            elif response.status_code == 500:
                print(f"Error occurred at {host} error: {response.json()['error']}")
            else:
                # Handle HTTP errors
                response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error occurred: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error occurred while connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout occurred: {errt}")

    return None


if __name__ == "__main__":
    json=get_workspace_json("/home/avinash/development/ReddyNet_V2.0","user_workspace")
    
    #remove the existing files
    os.system("rm -rf /home/avinash/development/ReddyNet_V2.0/server_workspace/*")

    server_workspace_creater("/home/avinash/development/ReddyNet_V2.0/server_workspace",json)


def save_workspace_ids(server_workspace_ids):
    """
    This function will save the workspace ids in a file, so that workspaces in the hosts can be reused,
    This function must only be called based on the user flag while running the main compiler
    If this function is called, then the workspaces also must not be deleted
    input: server_workspace_ids (dict)
    output: None, saves the workspace ids in a file in compiler workspace
    """

    path = workspace_data_path+"/server_workspace_ids.json"

    if not os.path.exists(workspace_data_path):
        os.mkdir(workspace_data_path)

    with open(path,"w") as f:
        f.write(json.dumps(server_workspace_ids))

    print(f"Workspace ids saved successfully to {path}")

    return None

def get_workspace_ids_from_file_or_hosts(hosts,workspace_path):
    """
    This function will get the workspace ids from the file or from the hosts based on scenario
    input: hosts (list of strings),workspace_path (string)
    output: server_workspace_ids (dict), gets the workspace ids from the file or from the hosts
    """

    path = workspace_data_path+"/server_workspace_ids.json"

    # check if the file exists
    if os.path.exists(path):

        # read the workspace ids from the file
        with open(path,"r") as f:
            server_workspace_ids=json.loads(f.read())

        workspace_not_present_but_in_file=[]

        # check if the workspaces are present in the hosts
        # if not present, then just remove the workspace id from the dict, the workspace will be sent again in next block
        for host in server_workspace_ids.keys():
            try:
                response = communication.get(f"{host}/workspace/check",json={"server_workspace_id":server_workspace_ids[host]})
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get("workspace_present"):
                        print(f"Reusing Workspace present in {host}")
                    else:
                        # workspace not present in the host
                        workspace_not_present_but_in_file.append(host)
                else:
                    # workspace not present in the host
                    workspace_not_present_but_in_file.append(host)
                    print(f"Error occurred at {host} error: {response.json()['error']}")
                    # Handle HTTP errors
                    response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error occurred: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error occurred while connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout occurred: {errt}")

        # remove the workspace ids which are not present in the hosts
        for host in workspace_not_present_but_in_file:
            del server_workspace_ids[host]

        # check if all the availaible hosts are present in the workspace ids
        if set(hosts) != set(server_workspace_ids.keys()):
            
            # send the workspace to the hosts which are not present in the workspace ids
            server_workspace_ids_new=send_workspace_to_hosts(list(set(hosts)-set(server_workspace_ids.keys())),workspace_path)

            # merge the new workspace ids with the existing workspace ids
            for key in server_workspace_ids_new.keys():
                server_workspace_ids[key]=server_workspace_ids_new[key]

            print("Workspace ids updated successfully")
    else:

        # file not found, so no workspace ids
        print("file not found for workspace ids, sending the workspace again to the hosts")

        # send the workspace to all the hosts
        server_workspace_ids=send_workspace_to_hosts(hosts,workspace_path)

    return server_workspace_ids

