#!/usr/bin/env python3
import os
import requests
api_key = "JUXT14RB9AIYHKT2MZTAWGP85UBH3Y6UER"
base_url = "https://api.etherscan.io/api?"

def is_valid_address(address):
    # Check that the address starts with "0x" and is 40 characters long
    if not (address.startswith("0x") and len(address) == 42):
        return False

    # Check that the address contains only hexadecimal characters
    try:
        int(address, 16)
        return True
    except ValueError:
        return False

def address_already_exists(address,lines):
    for line in lines:
        if line[1] == address:
            return True
    return False

def main():
    
    print('Enter name and associated address to be checked.\nThe name must not be empty.\nThe address must be a new, valid Ethereum address.\nProgram will populate "hashes.txt" with the most recent transactions automatically.\n\nEnter "quit" to exit the program.')
    if not os.path.exists('hashes.txt'):
        # Create the file if it does not exist
        with open('hashes.txt', 'w') as f:
            pass

    with open("hashes.txt", "r") as f:
        lines = [tuple(line.split()) for line in f]
    while True:
        # Get user input for name and address
        name = input("Name: ")
        # Check that the name is not empty
        while not name:
            print("Error: Please enter a name.")
            name = input("Name: ")
        # Replace any spaces in the name with a dash
        name = name.replace(" ", "-")
        # Check if the user entered "quit"
        if name.lower() == "quit":
            return 0
        
        address = input("Address: ")
        # Check that the address is a valid Ethereum address
        while not is_valid_address(address) or address_already_exists(address,lines):
            # Check if the user entered "quit"
            if address.lower() == "quit":
                return 0
            elif address_already_exists(address,lines):
                print("Error: Address already exists. Input a new address.")
                address = input("Address: ")
            else:
                print("Error: Please enter a valid Ethereum address.")
                address = input("Address: ")
        
        # Get the last hash for the specified address
        # Set the parameters for the API request to get the current block number
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": api_key
        }

        # Make the request to the Etherscan API
        response = requests.get(base_url, params=params)

        transaction_list = response.json()["result"][0]
        # print(transaction_list)
        # Compare the most recent transaction hashes, if new hash, notify user
        last_hash = transaction_list["hash"]

        # Get the last internal transaction hash
        internal_params= {
                        "module": "account",
                        "action": "txlistinternal",  # Use the tokennftx action
                        "address": address,
                        "sort": "desc",  # Set the sort order to "asc" to retrieve the transactions in chronological order
                        "apikey": api_key
                    }
        internal_response = requests.get(base_url, params=internal_params)
        internal_transaction_list = internal_response.json()["result"][0]
        # print(transaction_list)
        # Compare the most recent transaction hashes, if new hash, notify user
        last_internal_hash= internal_transaction_list["hash"]
        # Append a new line to the file with the name, address, and last transaction hash
        with open("hashes.txt", "a") as f:
            f.write(f"{name} {address} {last_hash} {last_internal_hash}\n")
        break


if __name__ == "__main__":
    main()
