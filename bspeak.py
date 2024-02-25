from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pickle

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_key_to_file(key, filename):
    with open(filename, "wb") as key_file:
        key_file.write(key)

def load_key_from_file(filename):
    with open(filename, "rb") as key_file:
        key = key_file.read()
    return key

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

def save_public_key(username, public_key):
    try:
        with open("public_keys.pkl", "rb") as f:
            public_keys = pickle.load(f)
    except FileNotFoundError:
        public_keys = {}
    public_keys[username] = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("public_keys.pkl", "wb") as f:
        pickle.dump(public_keys, f)

def load_public_key(username):
    with open("public_keys.pkl", "rb") as f:
        public_keys = pickle.load(f)
    return serialization.load_pem_public_key(public_keys[username], backend=default_backend())

def menu():
    print("1. Encrypt Message")
    print("2. Decrypt Message")
    print("3. Manage Keys")
    print("4. Exit")

def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            username = input("Enter recipient's username: ")
            message = input("Enter message to encrypt: ")
            public_key = load_public_key(username)
            encrypted_message = encrypt_message(message, public_key)
            print("Encrypted Message:", encrypted_message.hex())
        elif choice == "2":
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
            print("1. Generate Key Pair")
            print("2. Save Public Key")
            sub_choice = input("Enter your choice: ")
            if sub_choice == "1":
                private_key, public_key = generate_key_pair()
                private_key_file = input("Enter path to save your private key (e.g., /home/blackmagic/Desktop/private_key.pem): ")
                save_key_to_file(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ), private_key_file)
                print("Private Key saved successfully.")
                
                public_key_file = input("Enter path to save your public key (e.g., /home/blackmagic/Desktop/public_key.pem): ")
                save_key_to_file(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ), public_key_file)
                print("Public Key saved successfully.")
                
            elif sub_choice == "2":
                username = input("Enter username: ")
                public_key_file = input("Enter path to public key file: ")
                public_key = serialization.load_pem_public_key(
                    load_key_from_file(public_key_file),
                    backend=default_backend()
                )
                save_public_key(username, public_key)
                print("Public Key saved successfully.")
            else:
                print("Invalid choice.")
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
