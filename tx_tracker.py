#!/usr/bin/env python3
import requests
import time
import os
from pync import Notifier
import argparse
# def notify(title,text,link):
#     Notifier.notify(text,title = title,open=link)
# api_key = "JUXT14RB9AIYHKT2MZTAWGP85UBH3Y6UER"
base_url = "https://api.etherscan.io/api?"

# def save_last(last_hash):
#     with open("big_num.txt", "w") as f:
#         f.write(str(last_hash))
# def check_values(name,base_url,params,hash_info):
#          # Make the request to the Etherscan API
#         response = requests.get(base_url, params=params)

#         transaction_list = response.json()["result"][0]
#         # print(transaction_list)
#         # Compare the most recent transaction hashes, if new hash, notify user
#         transaction_id = transaction_list["hash"]
#         # print(transaction_id)
#         if transaction_id != hash_info[1]:

#             # Construct the link to the transaction
#             transaction_link = f"https://etherscan.io/tx/{transaction_id}"
            
#             # Get value of the transaction
#             transaction_value = float(transaction_list["value"])/1000000000000000000
#             if transaction_value == 0:
#                 transaction_value_formatted = "0"
#             else:
#                 transaction_value_formatted = "{:.6f}".format(transaction_value).rstrip('0').rstrip('.')

#             # Get the gas price of the transaction
#             transaction_gas_price = float(transaction_list["gasPrice"])/1000000000000000000
#             transaction_gas_price_formatted = "{:.10f}".format(transaction_gas_price).rstrip('0').rstrip('.')

#             # notify("New Transaction", f"There is a new transaction on the Ethereum account {address}.", transaction_link)
#             Notifier.notify(f"There is a new transaction on {name}.\nValue: {transaction_value_formatted} eth\nGas Price: {transaction_gas_price_formatted} eth",open=transaction_link)
#             return transaction_id

def save_last(all_hashes):
    with open("hashes.txt", "w") as f:
        # Iterate over the items in the dictionary
        for name, (address, last_hash,last_internal_hash) in all_hashes.items():
            # Write the name, address, and last transaction hash to the file
            f.write(f"{name} {address} {last_hash} {last_internal_hash}\n")
def main(args):
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
                    Notifier.notify(f"There is a new transaction on {name}.\nValue: {transaction_value_formatted} eth\nTransaction Fee: {transaction_fee_formatted} eth",open=transaction_link)
                    # all_hashes[name]=[hash_info[0],transaction_id,hash_info[2]]
                    print(name,hash_info[0],transaction_id,hash_info[2])
                time.sleep(args.buffer)
                if args.internal:
                    internal_params= {
                        "module": "account",
                        "action": "txlistinternal",  # Use the tokennftx action
                        "address": address,
                        "sort": "desc",  
                        "apikey": api_key
                    }

                    internal_response = requests.get(base_url, params=internal_params)
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
                        time.sleep(args.buffer+4)
                        # Notifier.notify(f"There is a new internal transaction on {name}.\nValue: {transaction_value_formatted_internal} eth\nGas Price: {transaction_gas_price_formatted_internal} eth",open=transaction_link_internal)
                        Notifier.notify(f"There is a new internal transaction on {name}.\nValue: {transaction_value_formatted_internal} eth\nGas Price: TDB eth",open=transaction_link_internal)
                        all_hashes[name]=[hash_info[0],transaction_id,transaction_id_internal]
                        print(name,hash_info[0],transaction_id,transaction_id_internal)
                    else:
                        all_hashes[name]=[hash_info[0],transaction_id,hash_info[2]]
    except KeyboardInterrupt:
        save_last(all_hashes)
        exit
if __name__ == "__main__":
    # Check if you've got an API key
    if not os.path.exists('api_key.txt'):
        print('"api_key.txt" file does not exist.') 
        print('Use "update_api.py" to get an API key.')
        exit
    api_key = open("api_key.txt").read()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--buffer", "-b", help="Time in seconds to wait between checks", type=float, default=1,required=False)
    argparser.add_argument("--internal", "-i", help="Update on internal transactions. Defaults to True.", type=bool, default = True, required=False)
    args = argparser.parse_args()
    main(args)