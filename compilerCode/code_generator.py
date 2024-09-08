

def seq_code_generator(r,tokens,seq_dollar_variables,seq_underscore_variables,imports_packages):

    """
    This function will execute the given code
    input:  r (redis)
            tokens (list of list of strings)
            seq_dollar_variables (list of strings)
            seq_underscore_variables (list of strings)
            imports_packages (strings)
    output: seq_code.py file with necessary code to execute the given code
    """

    # removing all $ from tokens
    for i in range(len(tokens)):                            # here we are removing all $ from the tokens
        for j in range(len(tokens[i])):                     # but should we remove only the first $ from variable names
            tokens[i][j] = tokens[i][j].replace("$","")     # and keep the rest of the $ in the tokens

    # removing all _ from tokens
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            tokens[i][j] = tokens[i][j].replace("_","")

    # writing the code to a file to execute
    with open('seq_cd/seq_code.py', 'w',encoding='utf-8') as file:

        # writing the import statements
        file.write(imports_packages+"\n")

        #writing json import statement
        file.write("import json\n")


        # writing redis import statement
        file.write("import redis\n")
        file.write("r = redis.Redis(host='localhost', port=6379)\n")

        variables = seq_dollar_variables + seq_underscore_variables

        # if this is second seq code block then get the variables from redis
        # checking if the variables are present in redis (this will be not valid for the first seq code block)
        
        for variable in variables:
            if r.exists(str(variable[1:])):
                file.write(f"{variable[1:]}=json.loads(r.get('{str(variable[1:])}'))\n")

        # writing the code

        for line_tokens in tokens:
            file.write("".join(line_tokens))
            file.write("\n")

        # writing the code to set the $variables after the code execution

        variables = seq_dollar_variables+seq_underscore_variables
        
        for i in range(len(variables)):
            file.write(f"r.set('{str(variables[i][1:])}',json.dumps({variables[i][1:]}))\n")
    
def par_code_generator(tokens,par_dollar_variables,par_underscore_variables,imports_packages,no_of_hosts):
    """
    This function will execute the given code
    input: tokens (list of list of strings)
           par_dollar_variables (list of strings)
           par_underscore_variables (list of strings)
           imports_packages (strings)
           no_of_hosts (int)
    output: par_code.py file with necessary code to execute the given code
    """
    # removing all $ from tokens
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            tokens[i][j] = tokens[i][j].replace("$","")

    # removing all _ from tokens
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            tokens[i][j] = tokens[i][j].replace("_","")

    
    for no in range(no_of_hosts):

        # writing the code to a file to execute
        with open(f'par_cd/par_code_{no}.py', 'w',encoding='utf-8') as file:

            # writing the import statements
            file.write(imports_packages+"\n")

            #writing json import statement
            file.write("import json\n")

            # writing redis import statement
            file.write("import redis\n")
            file.write("r = redis.Redis(host='localhost', port=6379)\n")

            # writing the code to get the $ variables
            # here the key would be variable name + $ + no but in code the variable name would be without $ and no
            variables = par_dollar_variables

            for variable in variables:
                file.write(f"{variable[1:]}=json.loads(r.get('{str(variable[1:])}${no}'))\n")

            # writing the code to get the _ variables
            # here the key would be just variable name since this is not divided among the hosts
            variables = par_underscore_variables

            for variable in variables:
                file.write(f"{variable[1:]}=json.loads(r.get('{str(variable[1:])}'))\n")
            
            # writing the user code
            for line_tokens in tokens:
                file.write("".join(line_tokens))
                file.write("\n")

            # writing the code to set the $variables after the code execution
            # here the key would be variable name + $ + no but in code the variable name would be without $ and no

            variables = par_dollar_variables
            for variable in variables:
                file.write(f"r.set('{str(variable[1:])}${no}',json.dumps({variable[1:]}))\n")

            # writing the code to set the _variables after the code execution
            # here the key would be just variable name since this is not divided among the hosts

            variables = par_underscore_variables
            for variable in variables:
                file.write(f"r.set('{str(variable[1:])}',json.dumps({variable[1:]}))\n")

            
