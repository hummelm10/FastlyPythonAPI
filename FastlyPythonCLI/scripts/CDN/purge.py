import scripts
import requests
import pprint
import pandas

def purgeKey(service, key, soft):
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        if soft:
            header.update({"Fastly-Soft-Purge":"1"})
        input("Request to be made: " + "https://api.fastly.com/service/" + str(service) + "/purge/" + str(key) + "\nPress Enter to continue...")    
        r=requests.post("https://api.fastly.com/service/" + str(service) + "/purge/" + str(key),headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            pprint.pprint(r.json())
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def purgeKeyMenu():
    df = scripts.listServicesNoPrint()
    print(df)
    try:
        sernumber = int(input("\n\nEnter index of service to purge: "))
    except:
        e = input("Not a valid number. Press enter to continue or E to exit...")
        if e.lower() == 'e':
            scripts.clear()
            purgeMenu()
    print(str(df.iloc[sernumber]))
    while "Not a valid response.":
        reply = str(input("Correct service [Y/n]: ")).lower().strip()
        if reply == 'y':
            service = str(df['ID'].iloc[sernumber])
            break
        if reply == 'n':
            scripts.clear()
            purgeKeyMenu()
            break
    key = str(input("Enter key to purge: "))
    print("Key: " + str(key))
    while "Not a valid response.":
        reply = str(input("Correct key [Y/n]: ")).lower().strip()
        if reply[0] == 'y':
            break
        if reply[0] == 'n':
            scripts.clear()
            purgeKeyMenu()
            break
    while "Not a valid response.":
        reply = str(input("Soft purge [Y/n]: ")).lower().strip()
        if reply[0] == 'y':
            purgeKey(service, key, True)
            break
        if reply[0] == 'n':
            purgeKey(service, key, False)
            break

def purgeService(service):
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        input("Request to be made: " + "https://api.fastly.com/service/" + str(service) + "/purge_all" + "\nPress enter to continue...")    
        r=requests.post("https://api.fastly.com/service/" + str(service) + "/purge_all",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            pprint.pprint(r.json())
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def purgeServiceMenu():
    df = scripts.listServicesNoPrint()
    print(df)
    try:
        sernumber = int(input("\n\nEnter index of service to purge: "))
        print(str(df.iloc[sernumber]))
    except:
        e = input("Not a valid number. Press enter to continue or E to exit...")
        if e.lower() == 'e':
            scripts.clear()
            purgeMenu()
    while "Not a valid response.":
        reply = str(input("Correct service [Y/n]: ")).lower().strip()
        if reply == 'y':
            service = str(df['ID'].iloc[sernumber])
            purgeService(str(service))
            break
        elif reply == 'n':
            scripts.clear()
            purgeKeyMenu()
            break

def purgeURL(url):
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        header.update({"Fastly-Soft-Purge":"1"})
        url = str(input("Purge URL: "))
        while "Not a valid response.":
            reply = str(input("Correct URL [Y/n]: ")).lower().strip()
            if reply == 'y':
                break
            elif reply == 'n':
                scripts.clear()
                purgeMenu()
                break
        r=requests.request("PURGE", str(url), headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            pprint.pprint(r.json())
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def purgeMenu():
    flag = True
    scripts.clear()
    while flag == True:
        scripts.clear()
        #Display menu options 
        print('  ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'PURGE MENU' + scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print('1: Purge Key')
        print('2: Purge Service')
        print('3: Purge URL')
        print('B to go back')
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print(' ')
        choice = input('Option: ').strip(' ')     #get user's choice

        if choice == '1':
            scripts.clear()
            purgeKeyMenu()
        elif choice == '2':
            scripts.clear()
            purgeServiceMenu()
        elif choice == '3':
            scripts.clear()
            try:
                url = str(input("Enter URL to purge: "))
            except:
                input("Error in input. Press Enter to continue...")
                scripts.clear()
                purgeMenu()
            purgeURL(url)
        elif choice.strip(' ') == 'B' or choice.strip(' ') == 'b':
            scripts.CDNMenu()
        else:
            input('Not a valid choice. Hit enter to continue...')