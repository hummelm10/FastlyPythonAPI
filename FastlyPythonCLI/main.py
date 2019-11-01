#import statments here
from os import system, name
import scripts
import requests
import shutil
import time

#global variables here
flag = True #loop control

columns = shutil.get_terminal_size().columns

if __name__ == "__main__":
    scripts.clear()
    print(('     ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'WELCOME TO THE FASTLY CLI' \
        + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "     ______           __  __         ________    ____" + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "    / ____/___ ______/ /_/ /_  __   / ____/ /   /  _/" + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "   / /_  / __ `/ ___/ __/ / / / /  / /   / /    / /  " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "  / __/ / /_/ (__  ) /_/ / /_/ /  / /___/ /____/ /   " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + " /_/    \__,_/____/\__/_/\__, /   \____/_____/___/   " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "                        /____/                       " + scripts.bcolors.ENDC).center(columns))


    print('This program will give you basic API controls for Fastly.') 
    time.sleep(3)
    scripts.clear()
    print('Checking if saved API Key is valid...')
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