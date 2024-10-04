""" 
This module will run the compiler on the given input file
"""
import os
import json
import sys
import redis
import compilerCode.code_handler as code_handler
import compilerCode.tokenizer as tokenizer
import compilerCode.code_generator as code_generator
import compilerCode.code_executor as code_executor
import compilerCode.code_verifier as code_verifier
import compilerCode.variable_handler as variable_handler
import compilerCode.environment_setup as environment_setup
import compilerCode.workspace_manager as workspace_manager

def compile_run(code,r,path_to_workspace,redis_string):

    """ 
    This function will compile the given code and run it.
    imputs: code: str: code to be compiled
            r: redis object: redis object
            path_to_workspace: str: path to the usrs workspace where the code is present
            redis_string: str:it is redis code to be added to the seq and par codes
    """

    # removing comments from the code
    code=code_handler.remove_comments(code)


    # separating the different components in the code
    hosts,multi_sequential_code,multi_parallel_code,path_to_req,imports_packages = code_handler.separate_code(code)

    # getting the no of hosts
    no_of_hosts = len(hosts)

    # sending workspace to all hosts
    server_workspace_ids=workspace_manager.send_workspace_to_hosts(hosts,path_to_workspace)

    # hosts recalculate, keeping only the hosts which have received the workspace
    hosts=server_workspace_ids.keys()

    # getting the no of hosts
    no_of_hosts = len(hosts)

    # adding one extra sequential code if the no of sequential and parallel code is not equal
    one_extra_seq = None

    if len(multi_sequential_code) != len(multi_parallel_code):
        one_extra_seq = multi_sequential_code[-1]
        multi_sequential_code = multi_sequential_code[:-1]

    # loop for each sequential and parallel code pair
    for sequential_code,parallel_code in zip(multi_sequential_code,multi_parallel_code):

        # Tokenizing the code
        seq_tokens = tokenizer.tokenize(sequential_code)
        par_tokens = tokenizer.tokenize(parallel_code)

        # Getting the variables used in the code linewise
        seq_dollar_variables_linewise,seq_underscore_variables_linewise = tokenizer.get_variables(seq_tokens)
        par_dollar_variables_linewise,par_underscore_variables_linewise = tokenizer.get_variables(par_tokens)

        # Getting the variables used in the code in a list
        seq_dollar_variables = tokenizer.get_variables_list(seq_dollar_variables_linewise)
        seq_underscore_variables = tokenizer.get_variables_list(seq_underscore_variables_linewise)
        par_dollar_variables = tokenizer.get_variables_list(par_dollar_variables_linewise)
        par_underscore_variables = tokenizer.get_variables_list(par_underscore_variables_linewise)


        # generating the sequential code
        code_generator.seq_code_generator(r,seq_tokens,seq_dollar_variables,seq_underscore_variables,imports_packages,hosts,redis_string)

        # installing the required packages
        # environment_setup.install_packages(path_to_req)      #until development same directory is used

        # executing the sequential code
        code_executor.seq_code_execute(r)

        # removing the installed packages
        # environment_setup.remove_packages(path_to_req)      #until development same directory is used
        
        # verify variables to be list,numpy or pandas dfs
        code_verifier.verify_dollar_variables(r,seq_dollar_variables)

        # devide and save variables for each host and get var type in a list,numpy or pandas dfs
        var_type=variable_handler.divide_variables_in_redis_no_of_hosts(r,seq_dollar_variables,no_of_hosts)

        # generating the parallel code
        code_generator.par_code_generator(par_tokens,par_dollar_variables,par_underscore_variables,imports_packages,no_of_hosts,redis_string)

        # executing the parallel code using servers on the hosts
        code_executor.server_par_code_executor(hosts,path_to_req,r,server_workspace_ids)

        # wait for all hosts to complete the execution
        code_executor.wait_for_all_hosts_to_complete(r,no_of_hosts)
        
        # merge variables from all hosts
        variable_handler.merge_variables_in_redis_no_of_hosts(r,par_dollar_variables,no_of_hosts,var_type)

    
    # delete all the workspaces in hosts after all parallel execution
    # workspace_manager.delete_workspace_in_hosts(hosts,server_workspace_ids)

    # if there is an extra sequential code
    if one_extra_seq:

        # Tokenizing the code
        seq_tokens = tokenizer.tokenize(one_extra_seq)

        # Getting the variables used in the code linewise
        seq_dollar_variables_linewise,seq_underscore_variables_linewise = tokenizer.get_variables(seq_tokens)

        # Getting the variables used in the code in a list
        seq_dollar_variables = tokenizer.get_variables_list(seq_dollar_variables_linewise)
        seq_underscore_variables = tokenizer.get_variables_list(seq_underscore_variables_linewise)

        # generating the sequential code
        code_generator.seq_code_generator(r,seq_tokens,seq_dollar_variables,seq_underscore_variables,imports_packages,hosts,redis_string)

        # installing the required packages
        # environment_setup.compile_install_packages(path_to_req)      #until development same directory is used

        # executing the sequential code
        code_executor.seq_code_execute(r)

        # removing the installed packages
        # environment_setup.compile_remove_packages(path_to_req)      #until development same directory is used

if __name__ == "__main__":
    print("Compiler started")

    # read config json
    with open("config.json","r") as f:
        config_json=f.read()

    config_json=json.loads(config_json)

    #redis
    red = redis.Redis(host=config_json['redis']['host'], port=config_json['redis']['port'], db=config_json['redis']['db'])
    path_to_workspace=config_json['user_workspace']['path']
    input_file=config_json['user_workspace']['nrp_file']
    redis_string=f'r = redis.Redis(host="{config_json["redis"]["host"]}", port="{config_json["redis"]["port"]}")\n'
    # Read the input file
    with open(path_to_workspace+"/"+input_file, 'r',encoding='utf-8') as file:
        input_file = file.read()
    compile_run(input_file,red,path_to_workspace,redis_string)
    