#import statments here
from os import system, name
import scripts
import requests

#global variables here
flag = True #loop control

if __name__ == "__main__":
    scripts.clear()
    print(scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'WELCOME TO THE FASTLY CLI' \
        + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
    print('This program will give you basic API controls for Fastly. Checking if saved API Key is valid...')
    scripts.checkAPI()
    while flag == True:
        scripts.clear()
        #Display menu options 
        print(' ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'MAIN MENU' + \
            scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print('1: Check API Key')
        print('2: Login/Generate API Key')
        print('3: List all active API Keys')
        print('4: WAF')
        print('5: CDN')
        print('Q to quit')
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print(' ')
        choice = input('Option: ')     #get user's choice

        if choice == '1':
            scripts.clear()
            scripts.checkAPI()
        elif choice == '2':
            scripts.clear()
            scripts.generateKey()
        elif choice == '3':
            scripts.clear()
            scripts.getAllTokens()
        elif choice == '4':
            scripts.clear()
            input("NO WAF OPTIONS YET")
        elif choice == '5':
            scripts.clear()
            scripts.CDNMenu()
        elif choice == 'Q' or choice == 'q':
            flag = False
        else:
            input('Not a valid choice. Hit enter to continue...')

    print('Program ending.')