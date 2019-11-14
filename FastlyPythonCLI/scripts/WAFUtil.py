import scripts

def WAFMenu():
    flag = True
    scripts.clear()
    while flag == True:
        scripts.clear()
        #Display menu options 
        print('  ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'WAF MENU' + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print('1: List/Search WAF Rules')
        print('2: List WAF IDs')
        print('3: List Service Active WAF Rules')
        print('4: OWASP')
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
        elif choice == 'B' or choice == 'b':
            flag = False
        else:
            input('Not a valid choice. Hit enter to continue...')