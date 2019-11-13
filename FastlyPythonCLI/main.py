#import statments here
from os import system, name
import requests
import shutil
import time
import signal
import pandas

#import custom 
import scripts

#definitions
def handler(signum, frame):
    print('Signal interrupt detected with signal (Ctrl-C): ', signum)
    exit()

#variables 
flag = True #loop control
columns = shutil.get_terminal_size().columns
signal.signal(signal.SIGINT, handler)
pandas.set_option('display.max_colwidth', -1)
pandas.set_option('display.max_rows', 1000)

if __name__ == "__main__":
    scripts.clear()
    print(('     ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'WELCOME TO THE FASTLY CLI' \
        + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "      ______           __  __         ________    ____ " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "     / ____/___ ______/ /_/ /_  __   / ____/ /   /  _/ " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "    / /_  / __ `/ ___/ __/ / / / /  / /   / /    / /   " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "   / __/ / /_/ (__  ) /_/ / /_/ /  / /___/ /____/ /    " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "  /_/    \__,_/____/\__/_/\__, /   \____/_____/___/    " + scripts.bcolors.ENDC).center(columns))
    print((scripts.bcolors.OKGREEN + "                         /____/                        " + scripts.bcolors.ENDC).center(columns))


    print(('This program will give you basic API controls for Fastly.').center(columns))
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
        print('1: WAF')
        print('2: CDN')
        print('3: List Services')
        print('4: Check API Key')
        print('5: Generate API Key')
        print('6: List API Keys')
        print('0: Revoke API Key')
        print('Q to quit')
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print(' ')
        choice = input('Option: ')     #get user's choice

        if choice == '1':
            scripts.clear()
            scripts.WAFMenu()
        elif choice == '2':
            scripts.clear()
            scripts.CDNMenu()
        elif choice == '3':
            scripts.clear()
            scripts.listServices()
        elif choice == '4':
            scripts.clear()
            scripts.checkAPI()
        elif choice == '5':
            scripts.clear()
            scripts.generateKey()    
        elif choice == '6':
            scripts.clear()
            scripts.getAllTokens()
        elif choice == '0':
            scripts.clear()
            scripts.revokeKey()
        elif choice == 'Q' or choice == 'q':
            flag = False
        else:
            input('Not a valid choice. Hit enter to continue...')

    print('Program ending.')