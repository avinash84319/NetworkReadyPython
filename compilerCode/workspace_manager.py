"""
This module will contain all the functions to handle the workspace in hosts
"""


import os
import requests

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
            response = requests.post(f"{host}/workspace",json=workspace_json)
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


if __name__ == "__main__":
    json=get_workspace_json("/home/avinash/development/ReddyNet_V2.0","user_workspace")
    
    #remove the existing files
    os.system("rm -rf /home/avinash/development/ReddyNet_V2.0/server_workspace/*")

    server_workspace_creater("/home/avinash/development/ReddyNet_V2.0/server_workspace",json)

