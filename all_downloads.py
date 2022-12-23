#!/usr/bin/env python3
import requests
import os
import pandas as pd
import openpyxl
import time
import argparse
from tqdm import tqdm
def get_transactions(addresses, api_key,args):
    transactions_list = []
    for address in tqdm(addresses, desc="Getting transactions"):
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

        # Make the request to the Etherscan API to get the transactions
        response = requests.get("https://api.etherscan.io/api", params=params)
        if response.json()["message"] == "No transactions found":
            tqdm.write(f"No transactions found for address {address} in the transactions.")
            time.sleep(args.delay)
        else:
            if response.status_code == 200:
                data = response.json()
                transactions = data["result"]
                # Read the data into a dataframe
                df = pd.DataFrame(transactions)
                # Convert the timestamp to a date
                df["Date"] = pd.to_datetime(df["timeStamp"], unit="s")
                # Convert the gas and gas price to ETH
                df["Gas"] = df["gas"].apply(lambda x: int(x) / 10**18)
                df["GasPrice"] = df["gasPrice"].apply(lambda x: int(x) / 10**18)
                # Convert the value to ETH
                df["Value"] = df["value"].apply(lambda x: int(x) / 10**18)
                # Extract the method name from the input data
                df["FunctionName"] = df["functionName"].apply(lambda x: x[:x.find("(")])

                # Select the relevant columns
                df = df[["Date", "from", "to", "hash", "Value", "Gas", "GasPrice", "FunctionName"]]
                # Rename the columns
                df.columns = ["Date", "From", "To", "Hash", "Value", "Gas", "GasPrice", "Method"]
                transactions_list.append(df)
            else:
                print("An error occurred:", response.status_code)
            time.sleep(args.delay)

    try:
        return pd.concat(transactions_list)
    except UnboundLocalError as e:
        print('No transactions found for any addresses, returning empty dataframe.')
        return pd.DataFrame()


def get_internal_transactions(addresses, api_key,args):
    transactions_list = []
    for address in tqdm(addresses, desc="Getting internal transactions"):
        params = {
        "module": "account",
        "action": "txlistinternal",  # Use the tokennftx action
        "address": address,
        "sort": "asc",  # Set the sort order to "asc" to retrieve the transactions in chronological order
        "apikey": api_key
    }

        # Make the request to the Etherscan API to get the internal transactions for the specified address
        response = requests.get("https://api.etherscan.io/api", params=params)
        if response.json()["message"] == "No transactions found":
            tqdm.write(f"No transactions found for address {address} in internal transactions.")
            time.sleep(args.delay)
        else:
            if response.status_code == 200:
                data = response.json()
                transactions = data["result"]
                # Read the data into a dataframe
                df = pd.DataFrame(transactions)
                # Convert the timestamp to a date
                df["Date"] = pd.to_datetime(df["timeStamp"], unit="s")
                # Convert the gas and gas used to ETH
                df["Gas"] = df["gas"].apply(lambda x: int(x) / 10**18)
                df["GasUsed"] = df["gasUsed"].apply(lambda x: int(x) / 10**18)
                # Convert the value to ETH
                df["Value"] = df["value"].apply(lambda x: int(x) / 10**18)
                # Select the relevant columns
                df = df[["Date", "from", "hash", "Value", "Gas", "GasUsed"]]
                # Rename the columns
                df.columns = ["Date", "From", "Hash", "Value", "Gas", "GasUsed"]
                transactions_list.append(df)
            else:
                print("An error occurred:", response.status_code)
            time.sleep(args.delay)
    try:
        return pd.concat(transactions_list)
    except UnboundLocalError as e:
        print('No internal transactions found for any addresses, returning empty dataframe.')
        return pd.DataFrame()


def get_erc20_transactions(addresses, api_key,args):
    transactions_list = []

    for address in tqdm(addresses, desc="Getting ERC20 transactions"):
        # Set the parameters for the API request to get the ERC20 transactions for the specified address
        params = {
            "module": "account",
            "action": "tokentx",  # Use the tokentx action
            "address": address,
            "sort": "asc",  # Set the sort order to "asc" to retrieve the transactions in chronological order
            "apikey": api_key
        }

        # Make the request to the Etherscan API to get the ERC20 transactions
        response = requests.get("https://api.etherscan.io/api", params=params)
        if response.json()["message"] == "No transactions found":
            tqdm.write(f"No transactions found for address {address} in the ERC20 module.")
            time.sleep(args.delay)
        else:
            if response.status_code == 200:
                data = response.json()
                transactions = data["result"]
                # Read the data into a dataframe
                df = pd.DataFrame(transactions)
                # Convert the timestamp to a date
                df["Date"] = pd.to_datetime(df["timeStamp"], unit="s")
                # Convert the gas and gas price to ETH
                df["Gas"] = df["gas"].apply(lambda x: int(x) / 10**18)
                df["GasPrice"] = df["gasPrice"].apply(lambda x: int(x) / 10**18)
                # Convert the value to the ERC20 token's unit (e.g., "wei" or "szabo")
                df["Value"] = df["value"].apply(lambda x: int(x) / 10**18)
                # Select the relevant columns
                df = df[["Date", "from", "to", "hash", "Value", "Gas", "GasPrice", "tokenName", "tokenDecimal"]]
                # Rename the columns
                df.columns = ["Date", "From", "To", "Hash", "Value", "Gas", "GasPrice", "NFTName", "NFTID"]
                transactions_list.append(df)
            else:
                print("An error occurred:", response.status_code)
            time.sleep(args.delay)
    try:
        return pd.concat(transactions_list)
    except UnboundLocalError as e:
        print('No ERC20 transactions found for any addresses, returning empty dataframe.')
        return pd.DataFrame()

def get_erc721_transactions(addresses, api_key,args):
    transactions_list = []
    for address in tqdm(addresses, desc="Getting ERC721 transactions"):
        # Set the parameters for the API request to get the ERC721 transactions for the specified address
        params = {
            "module": "account",
            "action": "tokennfttx",  # Use the tokennfttx action
            "address": address,
            "sort": "asc",  # Set the sort order to "asc" to retrieve the transactions in chronological order
            "apikey": api_key
        }

        # Make the request to the Etherscan API to get the ERC721 transactions
        response = requests.get("https://api.etherscan.io/api", params=params)
        if response.json()["message"] == "No transactions found":
            tqdm.write(f"No transactions found for address {address} in the ERC721 module.")
            time.sleep(args.delay)
        else:
            if response.status_code == 200:
                data = response.json()
                transactions = data["result"]
                # Read the data into a dataframe
                df = pd.DataFrame(transactions)
                # Convert the timestamp to a date
                df["Date"] = pd.to_datetime(df["timeStamp"], unit="s")
                # Convert the gas and gas price to ETH
                df["Gas"] = df["gas"].apply(lambda x: int(x) / 10**18)
                df["GasPrice"] = df["gasPrice"].apply(lambda x: int(x) / 10**18)
                # Convert the value to ETH (not applicable to ERC721 transactions)
                df["Value"] = 0
                # Select the relevant columns
                df = df[["Date", "from", "to", "hash", "Value", "Gas", "GasPrice", "tokenName", "tokenID"]]
                # Rename the columns
                df.columns = ["Date", "From", "To", "Hash", "Value", "Gas", "GasPrice", "NFTName", "NFTID"]
                transactions_list.append(df)
            else:
                print("An error occurred:", response.status_code)
            time.sleep(args.delay)
    try:
        return pd.concat(transactions_list)
    except UnboundLocalError as e:
        print('No ERC721 transactions found for any addresses, returning empty dataframe.')
        return pd.DataFrame()


def get_erc1155_transactions(addresses, api_key,args):
    transactions_list = []
    for address in tqdm(addresses, desc="Getting ERC1155 transactions"):
        # Set the parameters for the API request to get the ERC1155 transactions for the specified address
        params = {
            "module": "account",
            "action": "token1155tx",  # Use the tokennftx action
            "address": address,
            "sort": "asc",  # Set the sort order to "asc" to retrieve the transactions in chronological order
            "apikey": api_key
        }

        # Make the request to the Etherscan API to get the ERC1155 transactions
        response = requests.get("https://api.etherscan.io/api", params=params)
        if response.json()["message"] == "No transactions found":
            tqdm.write(f"No transactions found for address {address} in the ERC1155 module.")
            time.sleep(args.delay)
        else:
            if response.status_code == 200:
                data = response.json()
                transactions = data["result"]
                # Read the data into a dataframe
                df = pd.DataFrame(transactions)
                # Convert the timestamp to a date
                df["Date"] = pd.to_datetime(df["timeStamp"], unit="s")
                # Convert the gas and gas price to ETH
                df["Gas"] = df["gas"].apply(lambda x: int(x) / 10**18)
                df["GasPrice"] = df["gasPrice"].apply(lambda x: int(x) / 10**18)
                # Convert the value to ETH (not applicable to ERC1155 transactions)
                df["Value"] = 0
                # Select the relevant columns
                df = df[["Date", "from", "to", "hash", "Value", "Gas", "GasPrice", "tokenName", "tokenID"]]
                # Rename the columns
                df.columns = ["Date", "From", "To", "Hash", "Value", "Gas", "GasPrice", "NFTName", "NFTID"]
                transactions_list.append(df)
            else:
                print("An error occurred:", response.status_code)
            time.sleep(args.delay)
    
    try:
        return pd.concat(transactions_list)
    except UnboundLocalError as e:
        print('No ERC1155 transactions found for any addresses, returning empty dataframe.')
        return pd.DataFrame()

def main(args):
    # Check if api_key.txt exists
    if not os.path.exists('api_key.txt'):
        print('"api_key.txt" file does not exist.') 
        print('Use "update_api.py" to get an API key.')
        return 0
    api_key = open("api_key.txt").read()

    # Check if the file exists
    if not os.path.exists('my_addresses.txt'):
        print('"my_addresses.txt" file does not exist.') 
        print('Use "update_my_addresses.py" to add addresses to track.')
        return 0

    with open("my_addresses.txt") as f:
        addresses = f.readlines()

    # Strip the newline characters from each address
    addresses = [address.strip() for address in addresses]

    #Open the Excel spreadsheet, or create it if it does not exist
    if not os.path.exists("notebook.xlsx"):
        workbook = openpyxl.Workbook()
        workbook.save("notebook.xlsx")
    workbook = openpyxl.load_workbook("notebook.xlsx")

    transactions = get_transactions(addresses, api_key,args)
    internal_transactions = get_internal_transactions(addresses, api_key,args)
    erc20_transactions = get_erc20_transactions(addresses, api_key,args)
    erc721_transactions = get_erc721_transactions(addresses, api_key,args)
    erc1155_transactions = get_erc1155_transactions(addresses, api_key,args)

    # Write the data to the Excel spreadsheet
    with pd.ExcelWriter("notebook.xlsx", engine="openpyxl") as writer:
        transactions.to_excel(writer, sheet_name="Transactions", index=False)
        internal_transactions.to_excel(writer, sheet_name="Internal Transactions", index=False)
        erc20_transactions.to_excel(writer, sheet_name="ERC20 Transactions", index=False)
        erc721_transactions.to_excel(writer, sheet_name="ERC721 Transactions", index=False)
        erc1155_transactions.to_excel(writer, sheet_name="ERC1155 Transactions", index=False)
    # remove the first sheet
    workbook.remove(workbook.worksheets[0])

if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--delay", "-d", help="Amount of time to delay between api calls (in seconds). Default is 1 second.", type=float, default=1, required=False)
    args = argparse.parse_args()
    main(args)