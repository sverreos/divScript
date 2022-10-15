from urllib.request import urlopen
import hashlib
from termcolor import colored


def start():
    print("\n velg: \n 1: sha256 me passwd list \n")
    valg = int(input())
    
    if valg == 1:
        sha256PsswdList()
    else:
        print(colored("ugyldig input!",'red'))


def sha256PsswdList():
    sha256hash = input("[+] Enter sha256 Hash value: ")

    try:
        passwordList = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt').read(),'utf-8')
        for password in passwordList.split('\n'):
            guess = hashlib.sha256(bytes(password,'utf-8')).hexdigest()
            if guess == sha256hash:
                print(colored("\n [+] The password is: "+ str(password) + "\n \n",'green'))
                break
            elif guess != sha256hash:
                continue
            else:
                print (colored("\n The password does not mathched in the list... \n",'red'))
    except Exception as exc:
        print('There was a problem %s'%(exc))



start()