""" This module has all the helper functions to handle the source code """


def remove_comments(code):

    """
    This function will remove the comments from the code
    input: code (string)
    output: code (string)
    """

    code = code.split("\n")
    code = [i for i in code if i]

    #single line comments
    code = [i for i in code if i[0] != "#"]

    return "\n".join(code)


def separate_code(code):

    """
    This function will separate the sequential and parallel code
    input: code (string)
    output: hosts (list of strings),sequential_code (string), parallel_code (string)
    """

    code = code.split("\n")
    code = [i for i in code if i]

    multi_sequential_code = []
    multi_parallel_code = []

    sequential_code = []
    parallel_code = []
    hosts = []
    path_to_req=""
    imports_packages = []

    seq=0
    par=0
    hst=0
    pth=0
    ip=0

    for line in code:

        if line == "***":
            if hst == 0:
                hst=1
                continue

            if hst == 1:
                hst=0
                continue

        if line == ">>>":
            if pth == 0:
                pth=1
                continue

            if pth == 1:
                pth=0
                continue

        if line == "^^^":
            if ip == 0:
                ip=1
                continue

            if ip == 1:
                ip=0
                continue

        if line == "---":

            if seq == 0:
                seq=1
                continue

            if seq == 1:
                multi_sequential_code.append("\n".join(sequential_code))
                sequential_code = []
                seq=0
                continue
            
        if line == "|||":
            if par == 0:
                par=1
                continue

            if par == 1:
                multi_parallel_code.append("\n".join(parallel_code))
                parallel_code = []
                par=0
                continue

        if hst == 1:
            hosts.extend(line.split(","))

        if seq == 1:
            sequential_code.append(line)

        if par == 1:
            parallel_code.append(line)

        if pth == 1:
            path_to_req=line

        if ip == 1:
            imports_packages.append(line)

    # Removing the empty strings and quotes from the hosts
    hosts = [i[1:-1] for i in hosts if i!=""]

    return hosts,multi_sequential_code,multi_parallel_code,path_to_req,"\n".join(imports_packages)