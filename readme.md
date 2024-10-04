# Network Ready Python

Network Ready Python (NRP) is combination of tools which help python developers, escpecially Data or ML engineers to run distributed python code over multiple devices, without need of virtualization of these devices.

It allows users run thier code on different machines wherever they are in the world. It helps individual developers to share compute resources among themselfs.

## Features

- Run distributed python code
- Support for multiple sequential and parralel blocks
- Abstracts all the network and workspace management
- Environment managment at remote machines
- Supports distribution of List,Numpy arrays and pandas dataframes
- Automatic error handling for errors in remote machines

You just write a simple one file python like code with some NRP tokens added and everything else is managed by NRP from workspace sharing to execution.

## NRP txt file syntax docs :- [Syntax Guide](NRP_Syntax.md)
This txt file is like one main file which acts as both instruction and user code to run this tool and distributed python.

## Tech

NRP uses multiple other tools to implement the project

- Python
- Redis
- Pickle
- Shell
- Flask
- Poetry

Note ! :- Currently this supports only linux environment ( windows support coming soon )

Note ! :- Use virtual machines as much as possible if you dont know the code biegn executed by the server for safety . ( server can run code recieved from other users if ipaddress and ports are known)

## Installation ( Server at remote machines )

- Python
   Install [Python]
- Poetry
   Install [Poetry]
- NRP code
  Git clone this repo
    ```sh
    git clone https://github.com/avinash84319/NetworkReadyPython
    ```
- Poetry setup
     ```sh
     poetry install
     ```
- Environment
    ```sh
    poetry shell
    ```
    or use this brfore every command
    ```sh
    poetry run
    ```
- Run Flask Server
    ```sh
    flask --app servernode.py run --port 5000
    ```
This will create a flask server on the current machine which can accept distributed code to be run on this machine. ( do this wherever you want to run distributed code )

## Usage ( compiler at main machine )

Although the name is compiler it is not typical compiler , it just takes the NRP code converts it into suitable python code and manages everything else.

Note! :- Install everything which is needed for server in main machine also.

- Python
   Install [Python]
- Poetry
   Install [Poetry]
- NRP code
  Git clone this repo
    ```sh
    git clone https://github.com/avinash84319/ReddyNet_V2.0
    ```
- Poetry setup
     ```sh
     poetry install
     ```
- Environment
    ```sh
    poetry shell
    ```
    or use this brfore every command
    ```sh
    poetry run
    ```
- Run compiler
   ```sh
   python compiler.py <path to user workspace> <name of NRP txt file>
   ```
   for example
   ```sh
   python compiler.py /home/avinash/development/ReddyNet_V2.0/user_workspace input.txt
   ```
This will run the compiler and execute the code in all the remote machines specified in the NRP code.
The compiler makes all the HTTP requests to remote machine's NRP Flask servers for the execution.
   
Here the user workspace is Directory with all the necescary code files and modules to run the users code.
And the NRP txt file is like main code which will use all these files to execute.

[Python]:https://www.python.org/downloads/
[Poetry]:https://python-poetry.org/docs/#installation
