"""
This file is used to communicate with the servers.
It will be used to send the code to the servers and get the results back.
"""

import os
import json
import requests
import sys

user_token = os.getenv("USER_TOKEN")
user_id = os.getenv("USER_ID")

def post(url,json):
    """
    This function will send a post request to the server
    inputs: url: str: url of the server
            data: dict: data to be sent to the server
    outputs: response: dict: response from the server
    """
    response = requests.post(url, json=json , headers={"user-token": user_token, "user-id": user_id})

    if response.status_code == 401 and "message" in response.json():
        if response.json()["message"] == "Access denied":
            print("Access denied at the url ", url ,"check the user-token and user-id")
            print("User id: ", user_id)
            print("User token: ", user_token)
            sys.exit(1)
        
    return response


def get(url,json):
    """
    This function will send a get request to the server
    inputs: url: str: url of the server
            data: dict: data to be sent to the server
    outputs: response: dict: response from the server
    """
    response = requests.get(url, json=json , headers={"user-token": user_token, "user-id": user_id})

    if response.status_code == 401 and "message" in response.json():
        if response.json()["message"] == "Access denied":
            print("Access denied at the url ", url ,"check the user-token and user-id")
            print("User id: ", user_id)
            print("User token: ", user_token)
            sys.exit(1)

    return response