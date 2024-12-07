from dotenv import load_dotenv
import os

def environment_variable():

    """

    This function is used to check if the required environment variables are set.

    # Redis for Compiler
    REDIS_COMPILER_HOST=localhost
    REDIS_COMPILER_PORT=6379
    REDIS_COMPILER_DB=0
    
    # Redis for Server
    REDIS_SERVER_HOST=host.docker.internal
    REDIS_SERVER_PORT=6379
    REDIS_SERVER_DB=0
    
    # Base Path Configuration
    BASE_PATH=/workspaces
    BASE_PATH2=/home/avinash
    
    # User Workspace Configuration
    USER_WORKSPACE_PATH=${BASE_PATH2}/development/ReddyNet_V2.0/user_workspace
    USER_WORKSPACE_PATH2=${BASE_PATH}/NetworkReadyPython/user_workspace
    USER_WORKSPACE_NRP_FILE=input.txt
    
    # Server Workspace Configuration
    SERVER_WORKSPACE_PATH=${BASE_PATH2}/workspaces/serverworkspaces
    SERVER_WORKSPACE_PATH2=${BASE_PATH}/server_workspace
    
    # Compiler Workspace Configuration
    COMPILER_WORKSPACE_PATH=${BASE_PATH2}/workspaces/compilerworkspaces/
    COMPILER_WORKSPACE_PATH2=${BASE_PATH}/compiler_workspace
    
    # Rerun Configuration
    RERUN=True

    # delete config
    DELETE=True
    
    """
    print("Compiler started")

    load_dotenv()

    # check if the required environment variables are set
    
    #redis
    if os.getenv("REDIS_COMPILER_HOST") is None:
        raise Exception("REDIS_COMPILER_HOST is not set")
    if os.getenv("REDIS_COMPILER_PORT") is None:
        raise Exception("REDIS_COMPILER_PORT is not set")
    if os.getenv("REDIS_COMPILER_DB") is None:
        raise Exception("REDIS_COMPILER_DB is not set")
    if os.getenv("REDIS_SERVER_HOST") is None:
        raise Exception("REDIS_SERVER_HOST is not set")
    if os.getenv("REDIS_SERVER_PORT") is None:
        raise Exception("REDIS_SERVER_PORT is not set")
    if os.getenv("REDIS_SERVER_DB") is None:
        raise Exception("REDIS_SERVER_DB is not set")
    if os.getenv("BASE_PATH") is None:
        raise Exception("BASE_PATH is not set")
    if os.getenv("BASE_PATH2") is None:
        raise Exception("BASE_PATH2 is not set")
    if os.getenv("USER_WORKSPACE_PATH") is None:
        raise Exception("USER_WORKSPACE_PATH is not set")
    if os.getenv("USER_WORKSPACE_PATH2") is None:
        raise Exception("USER_WORKSPACE_PATH2 is not set")
    if os.getenv("USER_WORKSPACE_NRP_FILE") is None:
        raise Exception("USER_WORKSPACE_NRP_FILE is not set")
    if os.getenv("SERVER_WORKSPACE_PATH") is None:
        raise Exception("SERVER_WORKSPACE_PATH is not set")
    if os.getenv("SERVER_WORKSPACE_PATH2") is None:
        raise Exception("SERVER_WORKSPACE_PATH2 is not set")
    if os.getenv("COMPILER_WORKSPACE_PATH") is None:
        raise Exception("COMPILER_WORKSPACE_PATH is not set")
    if os.getenv("COMPILER_WORKSPACE_PATH2") is None:
        raise Exception("COMPILER_WORKSPACE_PATH2 is not set")
    if os.getenv("RERUN") is None:
        raise Exception("RERUN is not set")
    if os.getenv("DELETE") is None:
        raise Exception("DELETE is not set")

    return True
