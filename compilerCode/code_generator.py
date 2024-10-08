"""
This file contains the code to generate the code for the given code block
"""

from compilerCode import tokenizer

import os
import json

# read config json
with open("config.json","r") as f:
    config_json=f.read()
config_json=json.loads(config_json)

workspace_data_path=config_json['compiler_workspace']['path']

def seq_code_generator(r,tokens,seq_dollar_variables,seq_underscore_variables,imports_packages,hosts,redis_string):

    """
    This function will add necessary code to the given sequential code to execute
    input:  r (redis)
            tokens (list of list of strings)
            seq_dollar_variables (list of strings)
            seq_underscore_variables (list of strings)
            imports_packages (strings)
            hosts (list of strings)
            redis_string
    output: seq_code.py file with necessary code to execute the given code
    """
    
    # removing all $$,?? from tokens

    tokens=tokenizer.remove_compiler_tokens_from_variables(tokens)

    if not os.path.exists(workspace_data_path+'seq_cd'):
        os.makedirs(workspace_data_path+'seq_cd')

    # writing the code to a file to execute
    with open(workspace_data_path+'seq_cd/seq_code.py', 'w',encoding='utf-8') as file:

        # writing the import statements
        file.write(imports_packages+"\n")

        #writing json import statement
        file.write("from compilerCode import data_serializer\n")

        # writing redis import statement
        file.write("import redis\n")
        file.write(redis_string)

        # writing the code to set the flags for the host execution
        # since this is sequential code and parallel code will execute after this setting all to 0

        for host_no in range(len(hosts)):
            file.write(f"r.set('flag_for_host_execution_{host_no}',0)\n")

        variables = seq_dollar_variables + seq_underscore_variables

        # if this is second seq code block then get the variables from redis
        # checking if the variables are present in redis (this will be not valid for the first seq code block)
        
        for variable in variables:
            if r.exists(str(variable[2:])):
                file.write(f"{variable[2:]}=data_serializer.deserialize_data(r.get('{str(variable[2:])}'))\n")

        # writing the code

        for line_tokens in tokens:
            file.write("".join(line_tokens))
            file.write("\n")

        # writing the code to set the $variables after the code execution

        variables = seq_dollar_variables+seq_underscore_variables
        
        for i in range(len(variables)):
            file.write(f"r.set('{str(variables[i][2:])}',data_serializer.serialize_data({variables[i][2:]}))\n")
    
def par_code_generator(tokens,par_dollar_variables,par_underscore_variables,imports_packages,no_of_hosts,redis_string):
    """
    This function will execute the given code
    input: tokens (list of list of strings)
           par_dollar_variables (list of strings)
           par_underscore_variables (list of strings)
           imports_packages (strings)
           no_of_hosts (int)
           redis_string
    output: par_code.py file with necessary code to execute the given code
    """

    # removing all $$,?? from tokens

    tokens=tokenizer.remove_compiler_tokens_from_variables(tokens)

    if not os.path.exists(workspace_data_path+'par_cd'):
        os.makedirs(workspace_data_path+'par_cd')
    
    for no in range(no_of_hosts):

        # writing the code to a file to execute
        with open(workspace_data_path+f'par_cd/par_code_{no}.py', 'w',encoding='utf-8') as file:

            # #for testing error adding some bad code
            # if no==1:
            #     file.write("print(a)")

            # writing the import statements
            file.write(imports_packages+"\n")

            #writing json import statement
            file.write("from compilerCode import data_serializer\n")

            # writing redis import statement
            file.write("import redis\n")
            file.write(redis_string)

            # writing the code to set the flag for the host execution
            file.write(f"r.set('flag_for_host_execution_{no}',1)\n")

            # writing the code to get the $ variables
            # here the key would be variable name + $ + no but in code the variable name would be without $ and no
            variables = par_dollar_variables

            for variable in variables:
                file.write(f"{variable[2:]}=data_serializer.deserialize_data(r.get('{str(variable[2:])}${no}'))\n")

            # writing the code to get the _ variables
            # here the key would be just variable name since this is not divided among the hosts
            variables = par_underscore_variables

            for variable in variables:
                file.write(f"{variable[2:]}=data_serializer.deserialize_data(r.get('{str(variable[2:])}'))\n")
            
            # writing the user code
            for line_tokens in tokens:
                file.write("".join(line_tokens))
                file.write("\n")

            # writing the code to set the $$variables after the code execution
            # here the key would be variable name + $ + no but in code the variable name would be without $ and no

            variables = par_dollar_variables
            for variable in variables:
                file.write(f"r.set('{str(variable[2:])}${no}',data_serializer.serialize_data({variable[2:]}))\n")

            # writing the code to set the ??variables after the code execution
            # here the key would be just variable name since this is not divided among the hosts

            variables = par_underscore_variables
            for variable in variables:
                file.write(f"r.set('{str(variable[2:])}',data_serializer.serialize_data({variable[2:]}))\n")

            # writing the code to set the flag for the host execution after the code execution

            file.write(f"r.set('flag_for_host_execution_{no}',2)\n")

            
