#!/usr/bin/env python3
import requests
import time
import os
from pync import Notifier
import argparse

base_url = "https://api.etherscan.io/api?"

def new_internal_params(api_key,address,api_key_number):
    internal_params= {
        "module": "account",
        "action": "txlistinternal",  # Use the tokennftx action
        "address": address,
        "page": 1,
        "offset": 1,
        "sort": "desc",  
        "apikey": api_key[api_key_number]
    }
    internal_response = requests.get(base_url, params=internal_params)
    return internal_response

def new_params(api_key,address,api_key_number):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "page": 1,
        "offset": 1,
        "sort": "desc",
        "apikey": api_key[api_key_number]
    }
    response = requests.get(base_url, params=params)
    return response

def save_last(all_hashes):
    with open("hashes.txt", "w") as f:
        # Iterate over the items in the dictionary
        for name, (address, last_hash,last_internal_hash) in all_hashes.items():
            # Write the name, address, and last transaction hash to the file
            f.write(f"{name} {address} {last_hash} {last_internal_hash}\n")
def main(args,api_key,api_key_number):
    # Check if the file exists
    if not os.path.exists('hashes.txt'):
        # Create the file if it does not exist
        print('"hashes.txt" file does not exist.') 
        print('Use "add_hashes.py" to add addresses to track.')
        return 0
        # Read in the last saved values for your addresses of interest
    with open("hashes.txt", "r") as f:
        all_hashes = {}

        # Iterate over the lines in the file
        for line in f:
            # Split the line by the ':' character to get the name and hash
            name, address,last_hash,last_internal_hash = line.split()

            # Strip any leading or trailing white space from the name and hash
            name = name.strip()
            address = address.strip()
            last_hash = last_hash.strip()
            last_internal_hash = last_internal_hash.strip()

            # Append a tuple containing the name and hash to the list
            all_hashes[name]=[address,last_hash,last_internal_hash]
    try:

        while True:
            for name,hash_info in all_hashes.items():
                # Set the base URL for the Etherscan API
                
                # Set the address and API key
                address = hash_info[0]
                # Set the parameters for the API request to get the current block number
                params = {
                    "module": "account",
                    "action": "txlist",
                    "address": address,
                    "page": 1,
                    "offset": 1,
                    "sort": "desc",
                    "apikey": api_key[api_key_number]
                }

                # Make the request to the Etherscan API
                response = requests.get(base_url, params=params)
                if response.json()["message"] == "NOTOK":
                        print('Too many requests, updating api key')
                        api_key_number = api_key_number + 1
                        if api_key_number>=len(api_key)-1:
                            api_key_number = 0
                        response = new_params(api_key,address,api_key_number)
                transaction_list = response.json()["result"][0]

                # print(transaction_list)
                # Compare the most recent transaction hashes, if new hash, notify user
                transaction_id = transaction_list["hash"]
                # print(transaction_id)
                if transaction_id != hash_info[1]:

                    # Construct the link to the transaction
                    transaction_link = f"https://etherscan.io/tx/{transaction_id}"
                    
                    # Get value of the transaction
                    transaction_value = float(transaction_list["value"])/1000000000000000000
                    if transaction_value == 0:
                        transaction_value_formatted = "0"
                    else:
                        transaction_value_formatted = "{:.6f}".format(transaction_value).rstrip('0').rstrip('.')

                    # Get the gas price of the transaction
                    transaction_gas_price = float(transaction_list["gasPrice"])
                    transaction_gas_used = float(transaction_list["gasUsed"])
                    transaction_fee_formatted = "{:.10f}".format((transaction_gas_price*transaction_gas_used)/1000000000000000000).rstrip('0').rstrip('.')

                    # notify("New Transaction", f"There is a new transaction on the Ethereum account {address}.", transaction_link)
                    Notifier.notify(f"There is a new transaction on {name}.\nValue: {transaction_value_formatted} eth\nTransaction Fee: {transaction_fee_formatted} eth",
                    title='Etherscan',
                    open=transaction_link)
                    # all_hashes[name]=[hash_info[0],transaction_id,hash_info[2]]
                    print(name,hash_info[0],transaction_id,hash_info[2])
                time.sleep(args.buffer)
                if args.internal:
                    internal_params= {
                        "module": "account",
                        "action": "txlistinternal",  # Use the tokennftx action
                        "address": address,
                        "page": 1,
                        "offset": 1,
                        "sort": "desc",  
                        "apikey": api_key[api_key_number]
                    }

                    internal_response = requests.get(base_url, params=internal_params)
                    if internal_response.json()["message"] == "NOTOK":
                        print('Too many requests, updating api key')
                        api_key_number = api_key_number + 1
                        if api_key_number>=len(api_key)-1:
                            api_key_number = 0
                        internal_response = new_internal_params(api_key,address,api_key_number)
                    transaction_list_internal = internal_response.json()["result"][0]

                    # Compare the most recent transaction hashes, if new hash, notify user
                    transaction_id_internal = transaction_list_internal["hash"]
                    if transaction_id_internal != hash_info[2]:

                        # Construct the link to the transaction
                        transaction_link_internal = f"https://etherscan.io/tx/{transaction_id_internal}"
                        
                        # Get value of the transaction
                        transaction_value_internal = float(transaction_list_internal["value"])/1000000000000000000
                        if transaction_value_internal == 0:
                            transaction_value_formatted_internal = "0"
                        else:
                            transaction_value_formatted_internal = "{:.6f}".format(transaction_value_internal).rstrip('0').rstrip('.')

                        # # Get the gas price of the transaction
                        # transaction_gas_price_internal = float(transaction_list_internal["gasPrice"])/1000000000000000000
                        # transaction_gas_price_formatted_internal = "{:.10f}".format(transaction_gas_price_internal).rstrip('0').rstrip('.')
                        
                        # Notifier.notify(f"There is a new internal transaction on {name}.\nValue: {transaction_value_formatted_internal} eth\nGas Price: {transaction_gas_price_formatted_internal} eth",open=transaction_link_internal)
                        Notifier.notify(f"There is a new internal transaction on {name}.\nValue: {transaction_value_formatted_internal} eth\nGas Price: TDB eth",
                        title='Etherscan',
                        open=transaction_link_internal)
                        all_hashes[name]=[hash_info[0],transaction_id,transaction_id_internal]
                        print(name,hash_info[0],transaction_id,transaction_id_internal)
                    else:
                        all_hashes[name]=[hash_info[0],transaction_id,hash_info[2]]
                    time.sleep(args.buffer)
    # add in the exception for when the user presses ctrl+c or when there is a TypeError
    except (KeyboardInterrupt,TypeError) as e:
        if isinstance(e,KeyboardInterrupt):
            save_last(all_hashes)
            exit
        else:
            save_last(all_hashes)
            Notifier.notify(f"Too many api requests,update api key with update_api.py",
                        title='Etherscan')
            exit

if __name__ == "__main__":
    # Check if you've got an API key
    if not os.path.exists('api_key.txt'):
        print('"api_key.txt" file does not exist.') 
        print('Use "update_api.py" to get an API key.')
        exit
    # Read each line of the file and store it in a list
    api_key = []
    for line in open('api_key.txt'):
        api_key.append(line.strip())
    api_key_number = 0
    # api_key = open("api_key.txt").read()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--buffer", "-b", help="Time in seconds to wait between checks", type=float, default=1,required=False)
    argparser.add_argument("--internal", "-i", help="Update on internal transactions. Defaults to True.", type=bool, default = True, required=False)
    args = argparser.parse_args()
    main(args,api_key,api_key_number)