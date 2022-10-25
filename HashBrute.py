import itertools
from urllib.request import urlopen
import hashlib
from termcolor import colored
import sys
from hashlib import sha512
from random import choice, randint


def start():
    print("\n velg: \n 1: sha256 me passwd list \n 2: bruteforce sha256 \n 3: bruteforce md5 \n 4: bruteforce sha1 \n 5: sha512 med pswd list og wrapper\n")
    valg = int(input())
    
    if valg == 1:
        sha256PsswdList()
    elif valg == 2:
        bruteforceHash('sha256')
    elif valg== 3:
        bruteforceHash('md5')
    elif valg == 4:
        bruteforceHash('sha1')
    elif valg == 5:
        hashPswdListWithWrapper()
    else:
        print(colored("Ugyldig input!",'red'))


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

def hashPswdListWithWrapper():
    hashToCrack = input("enter hash to find: ")
    
    #[i.strip() for i in urlopen("https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt") if len(i) >= 12]
    try:
        passwordList = str(urlopen("https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt").read(),'utf-8')
        for password in passwordList.split('\n'):
            #guess = "ictf{"+password.upper+"}"
            guess = password
            #print(f"trying: {guess}")
            guess = hashlib.sha512(bytes(guess,'utf-8')).hexdigest()
            
            hashedguess = sha512(guess.encode()).hexdigest()
            if hashToCrack == guess:
                print(colored(f"the correct word: {password}",'green'))
                break
            elif hashToCrack != guess:
                print("elif")
                #continue
            else:
                print(colored(f"\n the password does  not match in the list...\n"),'red')
    except Exception as exc:
        print('There was a problem %s'%(exc))        



#words = [i.strip() for i in open("google-10000-english-no-swears.txt") if len(i) >= 12]
#flag = f"ictf{{{choice(words)}{choice(words).upper()}{'%02d'%randint(0,99)}}}"
#print(sha512(flag.encode()).hexdigest())

# 79959ceac451e42088f978040729eb266b7d2818eafcc1b71072e8050f71cf4ead9d5dcbdbf539c2f45ec63f313e43166502899057d461cfe2ca4df15b59b27e




def bruteforceHash(hashtype):
    wordlist = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+{}:;',./?-="
    y=''
    length=1
    wordlistHash=''
    passwordHash = input("Enter the Hash to bruteforce: ")

    while wordlistHash != passwordHash:
        for c in itertools.product(wordlist, repeat = length):
            word = y.join(c)
            if hashtype == 'sha256':
                wordlistHash = hashlib.sha256(word.encode('utf-8')).hexdigest()
                print(f"Trying password: {word}:{wordlistHash}")
                if wordlistHash == passwordHash:
                    print(colored(f"Found password : {word}",'green'))
                    break
            elif hashtype == 'md5':
                wordlistHash = hashlib.md5(word.encode("utf-8")).hexdigest()
                print(f"Trying password: {word}: {wordlistHash}")
                if wordlistHash == passwordHash:
                    print(colored(f"Found password : {word}",'green'))
                    break
            elif hashtype == 'sha1':
                wordlistHash = hashlib.sha1(word.encode("utf-8")).hexdigest()
                print(f"Trying password: {word}:{wordlistHash}")
                if wordlistHash == passwordHash:
                    print(colored(f"Found password : {word}",'green'))
                    break
            else:
                print(colored("Please enter a valid hash for the chosen hashtype",'red'))



#def bruteWithRockyou():
    #https://towardsdev.com/building-a-hash-cracking-tool-using-python-ea15768409ef
 #   textTobreak = input("enter text to bruteforce: ")




start()