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
    imputs: code: from request: code to be executed
    outputs: message: str: message of the execution
    """
    code = request.json.get("code")

    print(code)
    
    code_executor.par_code_execute(code)
    
    return jsonify({"message": "Code executed successfully"})


if __name__ == "__main__":
    app.run(debug=True)
