from flask import Flask, request, jsonify
import uuid
import os
import json
from functools import wraps
from dotenv import load_dotenv, dotenv_values
import redis

import compilerCode.code_executor as code_executor
import compilerCode.environment_setup as environment_setup
import compilerCode.workspace_manager as workspace_manager

load_dotenv()

app = Flask(__name__)

workspace_data_path = os.getenv("SERVER_WORKSPACE_PATH")

if not os.path.exists(workspace_data_path):
    os.makedirs(workspace_data_path)
    print("Server workspace directory created")


def authenticate(f):
    """Decorator to check for user-token and user-id in headers."""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_token = request.headers.get("user-token")
        user_id = request.headers.get("user-id")
        
        # Replace this logic with your actual token and user ID validation
        if not user_token or not user_id or not validate_user(user_token, user_id):
            return jsonify({"message": "Access denied"}), 401

        return f(*args, **kwargs)
    
    return decorated_function


def validate_user(user_token, user_id):
    """Validate the user-token and user-id.
    Replace with actual validation logic, such as database or cache lookup."""
    # Example dummy validation
    return user_token == os.getenv("USER_TOKEN") and user_id == os.getenv("USER_ID")


@app.route("/")
@authenticate
def home():
    return "ReddyNet server at your service!"


@app.route("/workspace", methods=["POST"])
@authenticate
def workspace():
    workspace_json = request.json
    path_to_save = workspace_data_path

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    # Create the id for the workspace
    id = str(uuid.uuid4())
    path_to_save = path_to_save + "/" + id

    try:
        workspace_manager.server_workspace_creater(path_to_save, workspace_json)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Workspace created successfully", "id": id})


@app.route("/workspace/delete", methods=["POST"])
@authenticate
def delete_workspace():
    id = request.json['server_workspace_id']

    try:
        os.system("chmod +x clear_poetry_env.sh")
        os.system("./clear_poetry_env.sh " + workspace_data_path + "/" + id + "/user_workspace/" + "pyproject.toml")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        os.system("rm -rf " + workspace_data_path + "/" + id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Workspace deleted successfully"})


@app.route("/workspace/install/check", methods=["GET"])
@authenticate
def check_install():
    id = request.json['server_workspace_id']

    # Check directory of user workspace
    user_workspace = os.listdir(workspace_data_path + "/" + id)[0]

    if not os.path.exists(workspace_data_path + "/" + id + "/" + user_workspace + "/pyproject.toml"):
        return jsonify({"message": "Packages not installed"}), 500

    return jsonify({"message": "Packages installed"}), 200


@app.route("/workspace/install", methods=["POST"])
@authenticate
def install():
    try:
        req_file = request.json['req_file']
        id = request.json['server_workspace_id']

        if not os.path.exists(workspace_data_path + "/" + id):
            os.makedirs(workspace_data_path + "/" + id)

        # Check directory of user workspace
        user_workspace = os.listdir(workspace_data_path + "/" + id)[0]

        # Write the req_file to the req.txt
        with open(workspace_data_path + "/" + id + "/" + user_workspace + "/req.txt", "w") as file:
            file.write(req_file)

        # Setting up the environment
        environment_setup.server_install_packages(workspace_data_path + "/" + id + "/" + user_workspace + "/req.txt")

        return jsonify({"message": "Packages installed successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/execute", methods=["POST"])
@authenticate
def execute():
    code = request.json['code_file']
    id = request.json['server_workspace_id']

    # Write the code to the file
    if not os.path.exists(workspace_data_path + "/" + id):
        os.makedirs(workspace_data_path + "/" + id)

    # Check directory of user workspace
    user_workspace = os.listdir(workspace_data_path + "/" + id)[0]

    with open(workspace_data_path + "/" + id + "/" + user_workspace + "/parcode.py", "w") as file:
        file.write(code)

    try:
        # Write the deserializer code file inside the workspace
        deseriazer_code = ""
        with open("compilerCode/data_serializer.py") as file:
            deseriazer_code = file.read()

        if not os.path.exists(workspace_data_path + "/" + id + "/" + user_workspace + "/compilerCode"):
            os.makedirs(workspace_data_path + "/" + id + "/" + user_workspace + "/compilerCode")

        with open(workspace_data_path + "/" + id + "/" + user_workspace + "/compilerCode/data_serializer.py", "w") as file:
            file.write(deseriazer_code)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        # Create a sh script to execute the code
        with open(workspace_data_path + "/" + id + "/" + user_workspace + "/execute.sh", "w") as file:
            file.write("cd " + workspace_data_path + "/" + id + "/" + user_workspace + "\n")
            file.write("poetry run python parcode.py")
        
        # Execute the code
        os.system("sh " + workspace_data_path + "/" + id + "/" + user_workspace + "/execute.sh")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Code executed successfully"})


@app.route("/workspace/check", methods=["GET"])
@authenticate
def check_workspace():
    id = request.json['server_workspace_id']

    if not os.path.exists(workspace_data_path):
        print("Server workspace directory does not exist")
        return jsonify({"error": "Server path does not exist"}), 500

    if not os.path.exists(workspace_data_path + "/" + id):
        return jsonify({"workspace_present": False}), 200

    return jsonify({"workspace_present": True}), 200


if __name__ == "__main__":

    # check the redis server
    try:
        print("Connecting to redis server on", os.getenv("REDIS_SERVER_HOST"), os.getenv("REDIS_SERVER_PORT"))
        r = redis.Redis(host=os.getenv("REDIS_SERVER_HOST"), port=os.getenv("REDIS_SERVER_PORT"), db=0)
        r.ping()
        print("Redis server is running")
    except Exception as e:
        print(f"Error occurred while connecting to redis server: {str(e)}")
        exit(1)

    app.run(host="0.0.0.0")
