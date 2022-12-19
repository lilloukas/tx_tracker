#!/usr/bin/env python3
import os
def is_valid_hash(last_hash):
    # Check that the last transaction hash starts with "0x" and is 66 characters long
    if not (last_hash.startswith("0x") and len(last_hash) == 66):
        return False

    # Check that the last transaction hash contains only hexadecimal characters
    try:
        int(last_hash, 16)
        return True
    except ValueError:
        return False

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
    
    print("Enter name, address, and last transaction hash.\nThe name must not be empty.\nThe address must be a new, valid Ethereum address.\nThe last transaction hash must be a valid Ethereum transaction hash.\n\nEnter 'quit' to exit the program.")
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

        last_hash = input("Last Transaction Hash: ")
        # Check that the last transaction hash is a valid Ethereum transaction hash
        while not is_valid_hash(last_hash):
            if last_hash.lower() == "quit":
                return 0
            print("Error: Please enter a valid Ethereum transaction hash.")
            last_hash = input("Last Transaction Hash: ")

        # Append a new line to the file with the name, address, and last transaction hash
        with open("hashes.txt", "a") as f:
            f.write(f"{name} {address} {last_hash}\n")
        break


if __name__ == "__main__":
    main()
