""" 
This module will run the compiler on the given input file
"""
import redis
import compilerCode.code_handler as code_handler
import compilerCode.tokenizer as tokenizer
import compilerCode.code_generator as code_generator
import compilerCode.code_executor as code_executor
import compilerCode.code_verifier as code_verifier
import compilerCode.variable_handler as variable_handler


def compile_run(code=""):

    """ 
    This function will compile the given code and run it.
    """

    # connecting to redis
    r = redis.Redis(host='localhost', port=6379)

    # removing comments from the code
    code=code_handler.remove_comments(code)


    # separating the sequential and parallel code
    hosts, sequential_code, parallel_code = code_handler.separate_code(code)

    # getting the no of hosts
    no_of_hosts = len(hosts)

    # Tokenizing the code
    seq_tokens = tokenizer.tokenize(sequential_code)
    par_tokens = tokenizer.tokenize(parallel_code)

    # Getting the variables used in the code linewise
    seq_variables_linewise = tokenizer.get_variables(seq_tokens)
    par_variables_linewise = tokenizer.get_variables(par_tokens)

    # Getting the variables used in the code in a list
    seq_variables = tokenizer.get_variables_list(seq_variables_linewise)
    par_variables = tokenizer.get_variables_list(par_variables_linewise)

    # generating the sequential code
    code_generator.seq_code_generator(seq_tokens,seq_variables)

    # executing the sequential code
    code_executor.seq_code_execute(r,seq_variables)

    # verify variables to be list
    code_verifier.verify_dollar_variables(r,seq_variables)

    # devide and save variables for each host
    variable_handler.divide_variables_in_redis_no_of_hosts(r,seq_variables,no_of_hosts)

    # generating the parallel code
    code_generator.par_code_generator(par_tokens,par_variables,no_of_hosts)

    # executing the parallel code
    code_executor.par_code_execute(no_of_hosts)
    

if __name__ == "__main__":
    print("Compiler started")
    # Read the input file
    with open('input.txt', 'r',encoding='utf-8') as file:
        input_file = file.read()
    compile_run(input_file)
    