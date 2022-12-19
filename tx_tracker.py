#!/usr/bin/env python3
import requests
import os
import time
from pync import Notifier
# Define the notify function
# def notify(title, text, link):
#     # Display the notification
#     # os.system("""
#     #           osascript -e 'display notification "{}" with title "{}" actions ["Open Link"]'
#     #           """.format(text, title))
#     # Open the link when the notification is clicked
#     os.system(f"open -a '/Applications/Google Chrome.app' '{link}'")

# def notify(title,text,link):
#     Notifier.notify(text,title = title,open=link)
api_key = "JUXT14RB9AIYHKT2MZTAWGP85UBH3Y6UER"

# def save_last(last_hash):
#     with open("big_num.txt", "w") as f:
#         f.write(str(last_hash))

def save_last(all_hashes):
    with open("hashes.txt", "w") as f:
        # Iterate over the items in the dictionary
        for name, (address, last_hash) in all_hashes.items():
            # Write the name, address, and last transaction hash to the file
            f.write(f"{name} {address} {last_hash}\n")
def main():
        # Read in the last saved values for your addresses of interest
    with open("hashes.txt", "r") as f:
        all_hashes = {}

        # Iterate over the lines in the file
        for line in f:
            # Split the line by the ':' character to get the name and hash
            name, address,last_hash = line.split()

            # Strip any leading or trailing white space from the name and hash
            name = name.strip()
            address = address.strip()
            last_hash = last_hash.strip()

            # Append a tuple containing the name and hash to the list
            all_hashes[name]=[address,last_hash]
    try:

        while True:
            for name,hash_info in all_hashes.items():
                # Set the base URL for the Etherscan API
                base_url = "https://api.etherscan.io/api?"

                # Set the address and API key
                # address = "0xba19c073c28f203d9fe23eefefa01a6d2562360f"
                # address = "0xe749e9E7EAa02203c925A036226AF80e2c79403E"
                address = hash_info[0]
                
                # Set the parameters for the API request
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

                transaction_list = response.json()["result"]
                # Compare the most recent transaction hashes, if new hash, notify user
                transaction_id = transaction_list[0]["hash"]
                # print(transaction_id)
                if transaction_id != hash_info[1]:
                    # print("New Transaction")

                    # Get the transaction ID of the first transaction in the list
                    # transaction_id = transaction_list[0]["hash"]

                    # Construct the link to the transaction
                    transaction_link = f"https://etherscan.io/tx/{transaction_id}"

                    # # Print the link to the transaction
                    # print(transaction_link)

                    # notify("New Transaction", f"There is a new transaction on the Ethereum account {address}.", transaction_link)
                    Notifier.notify(f"There is a new transaction on {name}.",open=transaction_link)
                    all_hashes[name]=[hash_info[0],transaction_id]

                    time.sleep(1)
    except KeyboardInterrupt:
        save_last(all_hashes)
        exit
if __name__ == "__main__":
    main()