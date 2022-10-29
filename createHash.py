from cgitb import text
from hashlib import sha256, sha512, sha1, md5
import hashlib
from termcolor import colored


def start():
    print("velg type Hash som skal lages: \n 1)Create md5 \n 2) Create Sha1 \n 3) Create Sha256 \n 4) Create Sha512")
    valgt = int(input())

    if valgt == 1:
        createMd5()
    elif valgt == 2:
        createSha1()
    elif valgt == 3:
        createSha256()
    elif valgt == 4:
        createSha512()
    elif valgt == 5:
        print()


def createMd5():
    textToHash = input(f"skriv inn tekst som skal Hashes med md5: ")
    hashedText = hashlib.md5(textToHash.encode()).hexdigest()
    print(colored(f"md5 versjon av '{textToHash}' er: \n {hashedText}", "green"))

def createSha1():
    textToHash = input(f"Skriv inn tekst som skal Hashes med SHA 1: ")
    hashedText = hashlib.sha1(textToHash.encode()).hexdigest()
    print(colored(f"SHA1 versjon av : '{textToHash}' er: \n {hashedText}","green"))

def createSha256():
    textToHash = input("Skriv inn tekst som skal Hashes me SHA 256: ")
    hashedText = hashlib.sha256(textToHash.encode()).hexdigest()
    print(colored(f"SHA256 versjon av: '{textToHash}' er: \n {hashedText}","green"))
def createSha512():
    textToHash = input("Skriv inn tekst som skal Hashes me SHA 512: ")
    hashedText = hashlib.sha512(textToHash.encode()).hexdigest()
    print(colored(f"SHA 512 versjon av '{textToHash}' er: \n {hashedText}","green"))



start()