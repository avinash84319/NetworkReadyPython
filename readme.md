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

## Installation ( Server )

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
- Run Flask Server
    ```sh
    flask --app servernode.py run --port 5000
    ```
This will create a flask server on the current machine which can accept distributed code to be run on this machine.


    
    
 

[Python]:https://www.python.org/downloads/
[Poetry]:https://python-poetry.org/docs/#installation
