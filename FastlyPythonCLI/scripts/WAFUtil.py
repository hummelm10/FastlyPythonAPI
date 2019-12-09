import scripts

def WAFMenu():
    flag = True
    scripts.clear()
    while flag == True:
        scripts.clear()
        #Display menu options 
        print('  ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'WAF MENU' + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print('1: List/Search All WAF Rules')
        print('2: List WAF IDs')
        print('3: List/Modify WAF Config')
        print('4: List OWASP Config')
        print('5: Modify WAF Rules')
        print('911d: Disable WAF - EMERGENCY ONLY')
        print('911e: Enable WAF - EMERGENCY ONLY')
        print('B to go back')
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print(' ')
        choice = input('Option: ')     #get user's choice

        if choice == '1':
            scripts.clear()
            scripts.WAF.listWAFRules()
        elif choice == '2':
            scripts.clear()
            scripts.WAF.listWAFIDs()
        elif choice == '3':
            scripts.clear()
            scripts.WAF.getWAFRuleset()
        elif choice == '4':
            scripts.clear()
            scripts.WAF.OWASP()
        elif choice == '5':
            scripts.clear()
            scripts.WAF.modifyRules()
        elif choice == '911d':
            scripts.clear()
            scripts.WAF.disableWAF()
        elif choice == '911e':
            scripts.clear()
            scripts.WAF.enableWAF()
        elif choice == 'B' or choice == 'b':
            scripts.mainMenu()
        else:
            input('Not a valid choice. Hit enter to continue...')