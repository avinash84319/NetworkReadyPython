from flask import Flask, request, jsonify

import compilerCode.code_executor as code_executor

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

    exec(code,{}) # some strange issue with exec function when using list comprehension
    #checkout stack to understand
    
    return jsonify({"message": "Code executed successfully"})


if __name__ == "__main__":
    app.run(debug=True)
