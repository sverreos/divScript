from base64 import b64decode, b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad, pad
#from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes
from termcolor import colored

def start():
    print(colored("\n Ps:Data needs to be edited in code!",'red'))
    print("\n 1: AES CBC \n 2: create AES CBC\n")
    choice = int(input("make a choice: "))

    if choice == 1:
        aesCBC()
    elif choice == 2:
        createAesCBC()
    else:
        print("please enter a valid value :(")
        start()




def aesCBC():
    try:
        iv = b64decode('1vpv5wtN9YSruAo1F8RmHw==')
        ciphertext = b64decode('rSkw4++0Ovmyfjzry84I4A==')
        key = b64decode('RFhwPj6FQ6u/mrrwbpEOKQ==')
        cipher = AES.new(key,AES.MODE_CBC,iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        print(colored(f"decrypted message: \n {plaintext.decode()} \n", 'green'))


    except (ValueError, KeyError):
        print(colored('ERROR!!!','red'))

def createAesCBC():
    sensitiveData = input("enter the data to encrypt: ")
    key = get_random_bytes(16) #must be 16,24 or 32 bytes long
    cipher = AES.new(key, AES.MODE_CBC)
    cipherText = cipher.encrypt(pad(sensitiveData.encode(), AES.block_size))

    print(colored(f"iv: {b64encode(cipher.iv).decode('utf-8')}",'green'))
    print(colored(f"CipherText: {b64encode(cipherText).decode('utf-8')}",'green'))
    print(colored(f"key: {b64encode(key).decode('utf-8')}",'green'))



start()