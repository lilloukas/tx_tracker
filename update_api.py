#!/usr/bin/env python3
import os
import requests

def validate_api_key(api_key):
    try:
        response = requests.get("https://api.etherscan.io/api", params={"module": "account", "action": "balance", "address": "0x0000000000000000000000000000000000000000", "tag": "latest", "apikey": api_key})
        # If the request is successful (status code 200), the API key is valid
        return response.json()["result"] != "Invalid API Key"
    except:
        # If there was an error making the request, the API key is invalid
        return False

def get_api_key():
    api_keys = []
    if os.path.exists("api_key.txt"):
        with open("api_key.txt", "r") as f:
            for line in f:
                api_keys.append(line.strip())
    else:
        with open("api_key.txt", "w") as f:
            pass
    print(api_keys)
    print("=========================================")
    print("Welcome to the Etherscan API key updater!")
    print("If you don't have an Etherscan API key, you can get one here: https://etherscan.io/myapikey")
    print("If you want to quit, enter 'quit' at any time.")
    print("=========================================")
    api_key = False
    while not api_key:
        # Prompt the user to enter an API key
        api_key = input("Please enter your Etherscan API key: ")
        # Check if the user wants to quit
        if api_key.lower() == "quit":
            return 0
        # Validate the API key by making a test request to the Etherscan API
        if api_key in api_keys:
            print("API key already in file. Please try again.")
            api_key = False
        elif not validate_api_key(api_key):
            # If the API key is invalid, set it to an empty string
            # to trigger the reprompt
            print("Invalid API key. Please try again.")
            api_key = False
        else:
            api_keys.append(api_key)
            # If the API key is valid, save it to apiKey.txt
            print('API key validated and saved to "api_key.txt."')
            with open("api_key.txt", "w") as f:
                for key in api_keys:
                    f.write(f"{key}\n")
    return api_key



if __name__ == "__main__":
    get_api_key()