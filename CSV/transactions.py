#!/usr/bin/env python3
import requests
import datetime
import os
import re
def main():
    api_key = "JUXT14RB9AIYHKT2MZTAWGP85UBH3Y6UER"

    # Check if the file exists
    if not os.path.exists('my_addresses.txt'):
        # Create the file if it does not exist
        print('"my_addresses.txt" file does not exist.') 
        print('Use "add_hashes.py" to add addresses to track.')
        return 0

    with open("my_addresses.txt") as f:
        addresses = f.readlines()

    # Strip the newline characters from each address
    addresses = [address.strip() for address in addresses]

    # Open the CSV file for writing
    with open("transactions.csv", "w") as f:
        # Write the column headers
        f.write("Date,From,To,Hash,Value,Gas,GasPrice,Method\n")

        for address in addresses:
            # Set the parameters for the API request to get the transactions for the specified address
            params = {
                "module": "account",
                "action": "txlist",  # Use the tokennftx action
                "address": address,
                "startblock": 0,
                "endblock": 99999999,
                "sort": "asc",  # Set the sort order to "asc" to retrieve the transactions in chronological order
                "apikey": api_key
            }

            # Make the request to the Etherscan API to get the transactions for the specified address
            response = requests.get("https://api.etherscan.io/api", params=params)

            if response.status_code == 200:
                data = response.json()
                transactions = data["result"]
                # print(transactions)
                for transaction in transactions:
                    date = datetime.datetime.fromtimestamp(int(transaction["timeStamp"]))  # Convert the timestamp to a date
                    from_address = transaction["from"]
                    to_address = transaction["to"]
                    gas = int(transaction["gas"]) / 10**18  # Convert the gas to ETH
                    gas_price = int(transaction["gasPrice"]) / 10**18  # Convert the gas price to ETH
                    _hash = transaction["hash"]
                    value = int(transaction["value"]) / 10**18  # Convert the value to ETH

                    method = transaction["functionName"]
                    start_index = method.find("(")
                    method = method[:start_index]
                    
                    f.write(f"{date},{from_address},{to_address},{_hash},{value},{gas},{gas_price},{method}\n")
            else:
                print("An error occurred:", response.status_code)

if __name__ == "__main__":
    main() 
