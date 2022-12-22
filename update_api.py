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
    print("=========================================")
    print("Welcome to the Etherscan API key updater!")
    print("If you don't have an Etherscan API key, you can get one here: https://etherscan.io/myapikey")
    print("If you want to quit, enter 'quit' at any time.")
    print("=========================================")
    api_key = ""
    # Check if apiKey.txt already exists
    if os.path.exists("api_key.txt"):
        # If apiKey.txt exists, read the API key from the file
        with open("api_key.txt", "r") as f:
            api_key = f.read().strip()
        # Validate the API key by making a test request to the Etherscan API
        if validate_api_key(api_key):
            # If the API key is valid, ask the user if they want to replace it
            replace = input('A valid API key is already saved in "apiKey.txt" \nDo you want to replace it? (y/n) ')
            if replace.lower() == "y" or replace.lower() == "yes":
                # If the user wants to replace the API key, set api_key to an empty string
                # to trigger the prompt for a new API key
                api_key = ""
            else:
                # If the user doesn't want to replace the API key, return it
                return api_key
        else:
            # If the API key in apiKey.txt is invalid, set api_key to an empty string
            # to trigger the prompt for a new API key
            api_key = ""
    while not api_key:
        # Prompt the user to enter an API key
        api_key = input("Please enter your Etherscan API key: ")
        # Check if the user wants to quit
        if api_key.lower() == "quit":
            return ""
        # Validate the API key by making a test request to the Etherscan API
        if not validate_api_key(api_key):
            # If the API key is invalid, set it to an empty string
            # to trigger the reprompt
            print("Invalid API key. Please try again.")
            api_key = ""
        else:
            # If the API key is valid, save it to apiKey.txt
            print('API key validated and saved to "apiKey.txt."')
            with open("api_key.txt", "w") as f:
                f.write(api_key)
    return api_key



if __name__ == "__main__":
    get_api_key()