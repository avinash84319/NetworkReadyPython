

def seq_code_generator(tokens,variables):

    """
    This function will execute the given code
    input: tokens (list of list of strings)
           variables (list of strings)
    output: seq_code.py file with necessary code to execute the given code
    """

    # removing all $ from tokens
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            tokens[i][j] = tokens[i][j].replace("$","")

    # writing the code to a file to execute
    with open('seq_code.py', 'w',encoding='utf-8') as file:

        #writing json import statement
        file.write("import json\n")


        # writing redis import statement
        file.write("import redis\n")
        file.write("r = redis.Redis(host='localhost', port=6379)\n")

        # writing the code

        for line_tokens in tokens:
            file.write("".join(line_tokens))
            file.write("\n")

        # writing the code to set the $variables based on the no of hosts
        
        for i in range(len(variables)):
            file.write(f"r.set('{str(variables[i][1:])}',json.dumps({variables[i][1:]}))\n")

    
def par_code_generator(tokens,variables,no_of_hosts):
    """
    This function will execute the given code
    input: tokens (list of list of strings)
           variables (list of strings)
           no_of_hosts (int)
    output: par_code.py file with necessary code to execute the given code
    """
    # removing all $ from tokens
    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            tokens[i][j] = tokens[i][j].replace("$","")

    
    for no in range(no_of_hosts):

        # writing the code to a file to execute
        with open(f'par_cd/par_code_{no}.py', 'w',encoding='utf-8') as file:

            #writing json import statement
            file.write("import json\n")

            # writing redis import statement
            file.write("import redis\n")
            file.write("r = redis.Redis(host='localhost', port=6379)\n")

            # writing the code to get the $_variables
            for variable in variables:
                file.write(f"{variable[1:]}=json.loads(r.get('{str(variable[1:])}${no}'))\n")
            
            # writing the user code
            for line_tokens in tokens:
                file.write("".join(line_tokens))
                file.write("\n")


            
