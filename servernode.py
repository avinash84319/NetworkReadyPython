from flask import Flask, request, jsonify
import uuid

import compilerCode.code_executor as code_executor
import compilerCode.environment_setup as environment_setup
import compilerCode.workspace_manager as workspace_manager

app = Flask(__name__)

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
    path_to_save = "/home/avinash/development/ReddyNet_V2.0/server_workspace"

    #creating the id for the workspace
    id = str(uuid.uuid4())

    path_to_save = path_to_save + "/" + id

    try:
        workspace_manager.server_workspace_creater(path_to_save, workspace_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Workspace created successfully", "id": id})


@app.route("/execute", methods=["POST"])
def execute():

    """
    This function will execute the received code.
    imputs: code_file (file): file containing the code to be executed
    outputs: message: str: message of the execution
    """
    code = request.files['code_file'].read().decode("utf-8")
    req_file = request.files['req_file'].read().decode("utf-8")

    # write the req_file to the req.txt
    with open("server_cd/req.txt", "w") as file:
        file.write(req_file)

    print(code)

    # setting up the environment
    environment_setup.install_packages("server_cd/req.txt")

    try:
        exec(code,{}) # some strange issue with exec function when using list comprehension
        #checkout stackoverflow to understand the issue
    except Exception as e:
        return jsonify({"error": str(e)}),500

    # removing the installed packages
    # environment_setup.remove_packages("server_cd/req.txt")  #while development same directory is used
    
    return jsonify({"message": "Code executed successfully"})


if __name__ == "__main__":
    app.run(debug=True)
