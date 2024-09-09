"""
Code for setting up environment for the code execution.
"""

def read_req_file(path_to_req="reqfake.txt"):
    """
    This function will read the requirements file.
    inputs: path_to_req: str: path to the requirements file
    outputs: list: list of packages
    """
    with open(path_to_req, 'r') as file:
        return file.readlines()

def install_packages(path_to_req="reqfake.txt"):
    """
    This function will install the required packages.
    inputs: path_to_req: str: path to the requirements file
    """
    import os
    os.system(f'poetry add $(cat {path_to_req})')

def remove_packages(path_to_req="reqfake.txt"):
    """
    This function will remove the packages already installed.
    inputs: path_to_req: str: path to the requirements file
    """
    import os
    os.system(f'poetry remove $(cat {path_to_req})')