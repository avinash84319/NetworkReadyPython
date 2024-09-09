from flask import Flask, request, jsonify

import compilerCode.code_executor as code_executor
import compilerCode.environment_setup as environment_setup

app = Flask(__name__)

@app.route("/")
def home():
    return "ReddyNet server at your service!"

@app.route("/execute", methods=["POST"])
def execute():

    """
    This function will execute the received code.
    imputs: code_file (file): file containing the code to be executed
    outputs: message: str: message of the execution
    """
    code = request.files['code_file'].read()
    req_file = request.files['req_file'].read().decode("utf-8")

    # write the req_file to the req.txt
    with open("server_cd/req.txt", "w") as file:
        file.write(req_file)

    # setting up the environment
    environment_setup.install_packages("server_cd/req.txt")

    exec(code,{}) # some strange issue with exec function when using list comprehension
    #checkout stackoverflow to understand

    # removing the installed packages
    # environment_setup.remove_packages("server_cd/req.txt")  #while development same directory is used
    
    return jsonify({"message": "Code executed successfully"})


if __name__ == "__main__":
    app.run(debug=True)
