import os
import hashlib
import pbkdf2
from cryptography.fernet import Fernet
import base64
from db import configuration

#Create a salt to hash users' passwords
#Generate 60 random bytes
random_bytes = os.urandom(60)

#Combine the fixed string and random bytes
combined_value = configuration.key.encode('utf-8') + random_bytes

#Compute the SHA-256 hash of the combined value
salt = hashlib.sha256(combined_value).hexdigest().encode('ascii')

#Check if the file exists
if not os.path.exists('salt.txt'):
    #Write the salt value to a file
    with open('salt.txt', 'wb') as file:
        file.write(salt)
        print("The salt created successfully!")


#Create a symmetric key for encrypting passwords
def generateSymmetricKey():
    key = Fernet.generate_key()
    return base64.urlsafe_b64encode(key)


#Check if the file exists
if not os.path.exists('symmetric.txt'):
    #Write the key value to a file
    with open('symmetric.txt', 'wb') as file:
        file.write(generateSymmetricKey())
        print("The symmetric key created successfully!")