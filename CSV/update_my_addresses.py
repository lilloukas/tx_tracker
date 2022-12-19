import os

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
def main():
    print('Enter "quit" to exit the program.')
    # If my_addresses.txt does not exist, create it
    if not os.path.exists("my_addresses.txt"):
        with open("my_addresses.txt", "w") as f:
            pass

    # Read the existing addresses from the file
    with open("my_addresses.txt", "r") as f:
        existing_addresses = f.readlines()

    # Remove leading/trailing whitespace from the addresses
    existing_addresses = [address.strip() for address in existing_addresses]
    print(existing_addresses)
    # Flag variable to track whether the user has entered a valid address
    valid_address_entered = False

    # Keep prompting the user for an address until they enter a valid address or "quit"
    while not valid_address_entered:
        # Prompt the user for a new address
        new_address = input("Enter a new Ethereum address: ")

        # Check if the user wants to quit the program
        if new_address.lower() == "quit":
            print("Quitting program.")
            break
        if new_address in existing_addresses:
            print("Address already in file. Please try again.")
        # Check if the new address is valid and not already in the file
        elif is_valid_address(new_address):
            # Append the new address to the end of the file
            with open("my_addresses.txt", "a") as f:
                f.write(new_address + "\n")
                print(f"Successfully added address: {new_address}")
                valid_address_entered = True
        else:
            print("Invalid address. Please try again.")

if __name__ == "__main__":
    main()