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
    
def compile_install_packages(path_to_req="reqfake.txt"):
    """
    This function will install the required packages.
    inputs: path_to_req: str: path to the requirements file
    """
    import os

    os.system(f'poetry add $(cat {path_to_req})')

def compile_remove_packages(path_to_req="reqfake.txt"):
    """
    This function will remove the packages already installed.
    inputs: path_to_req: str: path to the requirements file
    """
    import os

    os.system(f'poetry remove $(cat {path_to_req})')

def server_install_packages(path_to_req="reqfake.txt"):
    """
    This function will install the required packages.
    inputs: path_to_req: str: path to the requirements file
    """
    import os

    dir_path = "/".join(path_to_req.split("/")[:-1])

    print(f'dir_path: {dir_path}')

    #creating shell script to install packages
    with open(f"{dir_path}/install.sh", "w") as file:
        file.write(f'cd {dir_path}\npoetry init --no-interaction\npoetry add $(cat {path_to_req})')

    #executing the shell script
    os.system(f'chmod +x {dir_path}/install.sh')
    os.system(f'sh {dir_path}/install.sh')

def server_remove_packages(path_to_req="reqfake.txt"):
    """
    This function will remove the packages already installed.
    inputs: path_to_req: str: path to the requirements file
    """
    import os
    
    dir_path = "/".join(path_to_req.split("/")[:-1])

    #creating shell script to remove packages
    with open(f"{dir_path}/remove.sh", "w") as file:
        file.write(f'cd {dir_path}\npoetry remove $(cat {path_to_req})')
    
    #executing the shell script
    os.system(f'chmod +x {dir_path}/remove.sh')
    os.system(f'{dir_path}/remove.sh')