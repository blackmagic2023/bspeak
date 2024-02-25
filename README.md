# bspeak
A message encryption and decryption script for secure 2-way communication.

#
![bspeak](https://github.com/blackmagic2023/blackspeak2/assets/149164084/812064d9-3f2b-46dd-b25a-9717e3ae1752)


# Setup

Download the script

```
git clone https://github.com/blackmagic2023/bspeak.git
```

Enter working directory

```
cd bspeak
```

# Features

- Generate key pair's
- Save users public key by username
- Fast and secure encryption

# Usage

Run the program

```
python3 bspeak.py
```

## Generating key pair

- When generating a key pair you must select option 3 in the menu 'manage keys' and option 1 in the manage key's menu 'generate key pair'

![gkey](https://github.com/blackmagic2023/blackspeak2/assets/149164084/12db6744-171e-4dac-9234-8c8519143e68)

- you should then be prompted to enter the path for your private and public keys. If you do not specify a directory the key files will be placed in your bspeak directory. When naming the file spaces are not allowd and the name must end with a .pem extension as seen in the image below.

![genkeys](https://github.com/blackmagic2023/blackspeak2/assets/149164084/50108d1a-40de-4338-b8f9-0b0621320e65)

## Adding users to message

- When you need to add a users public key you may do so by selecting option 3 in the main menu 'manage keys' once you are in the manage key menu select option 2 'save public key'

- Next you will be prompted for a username you can set any username for someone you have the public key for


![bobskey](https://github.com/blackmagic2023/blackspeak2/assets/149164084/e2fd695c-09fd-4404-82e4-721999e3be39)

## Encrypting a message

- Select option 1 from the main menu
- You should be prompted to enter a username
- type the username of a user you have defined in the program with a public key and username
- type a message
- send your encrypted message to the owner of the public key you added as a user!

![sendbob](https://github.com/blackmagic2023/blackspeak2/assets/149164084/b5f7bc18-27be-403d-8332-6aabdf042699)

## Decrypting a message

- If someone is using bspeak and has added you as a user and encrypted a message for you all you have to do is select option 2 'decrypt message' in the main menu
- you will be prompted to specify where your private key file is located
- next you will be prompted to enter th encrypted message

![dcrypt](https://github.com/blackmagic2023/blackspeak2/assets/149164084/b9cf7869-99f2-4a4c-b2b6-86f0b314ddbc)


enjoy <3

blackmagic


