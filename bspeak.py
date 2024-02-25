import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Function to save a key to a JSON file
def save_key_to_json(key, filename):
    with open(filename, "w") as key_file:
        json.dump(key, key_file)

# Function to load keys from a JSON file
def load_keys_from_json(filename):
    try:
        with open(filename, "r") as key_file:
            keys = json.load(key_file)
        return keys
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Unable to load keys from JSON file.")
        return {}

# Function to save the public key along with the username to a JSON file
def save_public_key_to_json(username, public_key):
    keys = load_keys_from_json("public_keys.json")
    keys[username] = public_key.decode()
    save_key_to_json(keys, "public_keys.json")

# Function to load the public key from the JSON file
def load_public_key_from_json(keys, username):
    if username in keys:
        return keys[username].encode()
    else:
        print("Error: Public key not found.")
        return None

# Function to generate a key pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Function to encrypt a message using a public key
def encrypt_message(message, public_key):
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

# Function to decrypt a message using a private key
def decrypt_message(encrypted_message, private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

# Main function
def main():
    keys = load_keys_from_json("public_keys.json")
    while True:
        print("1. Encrypt Message")
        print("2. Decrypt Message")
        print("3. Manage Keys")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Encrypt Message
            username = input("Enter recipient's username: ")
            message = input("Enter message to encrypt: ")
            public_key = load_public_key_from_json(keys, username)
            if public_key:
                encrypted_message = encrypt_message(message, public_key)
                print("Encrypted Message:", encrypted_message.hex())
            else:
                print("Error: Unable to load recipient's public key.")
        
        elif choice == "2":
            # Decrypt Message
            private_key_file = input("Enter path to your private key file: ")
            encrypted_message = bytes.fromhex(input("Enter encrypted message: "))
            private_key = serialization.load_pem_private_key(
                load_key_from_file(private_key_file),
                password=None,
                backend=default_backend()
            )
            decrypted_message = decrypt_message(encrypted_message, private_key)
            print("Decrypted Message:", decrypted_message)
        
        elif choice == "3":
            # Manage Keys
            print("1. Generate Key Pair")
            print("2. Save Public Key")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == "1":
                # Generate Key Pair
                private_key, public_key = generate_key_pair()
                private_key_file = input("Enter path to save your private key (e.g., private_key.pem): ")
                save_key_to_file(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ), private_key_file)
                print("Private Key saved successfully.")
                
                public_key_file = input("Enter path to save your public key (e.g., public_key.pem): ")
                save_key_to_file(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ), public_key_file)
                save_public_key_to_json(username, public_key)
                print("Public Key saved successfully.")
                
            elif sub_choice == "2":
                # Save Public Key
                username = input("Enter username: ")
                public_key_file = input("Enter path to public key file (e.g., public_key.pem): ")
                public_key = load_key_from_file(public_key_file)
                if public_key:
                    save_public_key_to_json(username, public_key)
                    print("Public Key saved successfully.")
                else:
                    print("Error: Unable to load public key file.")
            else:
                print("Invalid choice.")
        
        elif choice == "4":
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
