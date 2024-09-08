"""
This module contains the Tokenizer functions, which is used to tokenize the input text.
"""

ALPHABETS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
OPERATORS = ["+","-","*","/","%","=",">","<","!","&","|","^","~","?",".",",",";",":","(",")","[","]","{","}"]
KEYWORDS = ["print","if","push","else","elif","while","for","do","switch","case","break","continue","return","goto","define","include","import","from","as","class","def","try"]


def tokenize(code):

    """
    This function will tokenize the given code
    input: code (string)
    output: line_wise_tokens (list of list of strings)
    """

    tokens = [ list(line_tokens) for line_tokens in code.split("\n") ]

    return tokens

def get_symbol_variables(tokens,symbol="$"):

    """
    This function will return the variables used in the code
    input: tokens (list of list of strings)
    output: symbolvariables (list of list of strings)
    """

    variables = []

    for line_tokens in tokens:

        stack=[]
        line_variables = []

        for token in line_tokens:

            if token in ALPHABETS or token in NUMBERS or token=="_" or token==symbol:
                stack.append(token)

            if token in OPERATORS or token in [" ","\t","\n"]:
                if stack:
                    if "".join(stack) not in KEYWORDS and "".join(stack) not in line_variables:
                        if stack[0] not in NUMBERS:
                            line_variables.append("".join(stack))
                    stack=[]

        if stack:
            if "".join(stack) not in KEYWORDS and "".join(stack) not in line_variables:
                if stack[0] not in NUMBERS:
                    line_variables.append("".join(stack))
            stack=[]

        variables.append(line_variables)

    # Removing duplicates
    variables = [ list(set(line_variables)) for line_variables in variables ]

    # Removing the variables which are not starting with symbol
    variables = [ [ variable for variable in line_variables if variable[0]==symbol ] for line_variables in variables ]
    
    return variables

def get_variables(tokens):

    """
    This function will return the variables used in the code
    input: tokens (list of list of strings)
    output: $variables (list of list of strings)
            _variables (list of list of strings)
    """

    dollor_variables = get_symbol_variables(tokens,symbol="$")
    underscore_variables = get_symbol_variables(tokens,symbol="_")
    
    return dollor_variables,underscore_variables

    

def get_variables_list(variables_linewise):

    """
    This function will return the variables used in the code in a list
    input: variables_linewise (list of list of strings)
    output: variables (list of strings)
    """

    variables = []

    for line_variables in variables_linewise:

        for variable in line_variables:

            if variable not in variables:

                variables.append(variable)

    return variables