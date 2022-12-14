
from termcolor import colored
#from unittest import result


def start():
    print("velg type som skal gjøres om til text: \n 1 : hex \n 2: binary \n 3: octal \n 4: Xor two strings")
    valgt = int(input())
    if valgt == 1:
        result = hexToText()
    elif valgt == 2:
        result = binaryToText()
    elif valgt == 3:
        result = octalToString()
    elif valgt == 4:
        result = XorTwoStrings()
    else:
        print(colored("ugyldig nummer",'red'))

    print(colored("\n \n Ditt resultat: " + result + "\n \n",'green'))



def hexToText():
    #kjør scriptet og lim inn hexStrengen i kommandovinduet
    #eksempel streng: 616e696d6174696f6e
    hexString = input("\n Skriv inn hexStreng: ")


    textString = bytearray.fromhex(hexString).decode()
    result = textString
    return result
    #print("din input: ")
    #print(textString)



def binaryToText():
    #kjør script og lim in binærstreng i comandovindu
    #eksempel streng: 01110000 01100101 01100001 01110010
    binaryString =input("\n Input binary string: " )

    binaryValues = binaryString.split()

    asciiString=""

    for i in binaryValues:
        anInteger = int(i,2)
        asciiCharacter = chr(anInteger)
        asciiString += asciiCharacter

    result = asciiString
    return result
    #print("din input: ")
    #print(asciiString)



def octalToString():
    #kjør scriptet og lim in octal streng i kommandovindu
    # eksempel streng 154 151 155 145 
    octalString = input("\n Enter octal string: ")

    strConverted = ""
    for octalChar in octalString.split():
        strConverted += chr(int(octalChar,8))
    
    result = strConverted
    return result
    #print("Din input: ")
    #print(strConverted)

def XorTwoStrings():
    firstString = input("\n Enter the first string: ")
    secondString = input("\n Enter the second string: ")
    new = [chr(ord(a)^ ord(b)) for a,b in zip(firstString,secondString)]
    thirdString = "".join(new)
    result = thirdString
    return result


start()