import scripts

def CDNMenu():
    flag = True
    scripts.clear()
    while flag == True:
        scripts.clear()
        #Display menu options 
        print('  ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'CDN MENU' + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print('1: List Public IPs')
        print('2: Purge Options')
        print('3: Activate Service')
        print('B to go back')
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print(' ')
        choice = input('Option: ')     #get user's choice

        if choice == '1':
            scripts.clear()
            scripts.CDN.listPublicIPs()
        elif choice == '2':
            scripts.clear()
            scripts.CDN.purgeMenu()
        elif choice == '3':
            scripts.clear()
            scripts.CDN.activateService()
        elif choice == 'B' or choice == 'b':
            flag = False
        else:
            input('Not a valid choice. Hit enter to continue...')