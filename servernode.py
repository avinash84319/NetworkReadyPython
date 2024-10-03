from flask import Flask, request, jsonify
import uuid
import os

import compilerCode.code_executor as code_executor
import compilerCode.environment_setup as environment_setup
import compilerCode.workspace_manager as workspace_manager

app = Flask(__name__)

workspace_data_path="/workspaces/server_workspace"

@app.route("/")
def home():
    return "ReddyNet server at your service!"

@app.route("/workspace", methods=["POST"])
def workspace():
    """
    This function will create the workspace for the server
    inputs: workspace_json: dict: json containing the workspace information
    outputs: message: str: message of the workspace creation
    """
    workspace_json = request.json
    path_to_save = workspace_data_path

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    #creating the id for the workspace
    id = str(uuid.uuid4())

    path_to_save = path_to_save + "/" + id

    try:
        workspace_manager.server_workspace_creater(path_to_save, workspace_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Workspace created successfully", "id": id})

@app.route("/workspace/install/check", methods=["GET"])
def check_install():
    """
    This function will check if the packages are installed for the workspace
    inputs: id: str: id of the workspace
    outputs: message: str: message of the installation
    """

    id = request.json['server_workspace_id']

    # check directory of user workspace
    user_workspace = os.listdir(workspace_data_path+"/"+id)[0]

    if not os.path.exists(workspace_data_path+"/"+id+"/"+user_workspace+"/pyproject.toml"):
        return jsonify({"message": "Packages not installed"}), 500

    return jsonify({"message": "Packages installed"}), 200

@app.route("/workspace/install", methods=["POST"])
def install():
    """
    This function will install the packages for the workspace
    inputs: id: str: id of the workspace
    outputs: message: str: message of the installation
    """

    req_file = request.json['req_file']
    id = request.json['server_workspace_id']

    if not os.path.exists(workspace_data_path+"/"+id):
        os.makedirs(workspace_data_path+"/"+id)

    # check directory of user workspace
    user_workspace = os.listdir(workspace_data_path+"/"+id)[0]

    # write the req_file to the req.txt
    with open(workspace_data_path+"/"+id+"/"+user_workspace+"/req.txt", "w") as file:
        file.write(req_file)

    # setting up the environment
    environment_setup.server_install_packages(workspace_data_path+"/"+id+"/"+user_workspace+"/req.txt")

    return jsonify({"message": "Packages installed successfully"})


@app.route("/execute", methods=["POST"])
def execute():

    """
    This function will execute the received code.
    imputs: code_file (file): file containing the code to be executed
    outputs: message: str: message of the execution
    """
    
    code = request.json['code_file']
    id = request.json['server_workspace_id']

    try:
        exec(code,{}) # some strange issue with exec function when using list comprehension
        #checkout stackoverflow to understand the issue
    except Exception as e:
        return jsonify({"error": str(e)}),500

    # removing the installed packages
    # environment_setup.server_remove_packages(workspace_data_path+"/"+id+"/"+user_workspace+"/req.txt")  #while development same directory is used
    
    return jsonify({"message": "Code executed successfully"})


if __name__ == "__main__":
    app.run(debug=True)
