import requests
import scripts
import pprint
import pandas
from .listWAFIDs import listWAFIDsNoPrompt

def disableWAF():
    print(scripts.bcolors.FAIL + scripts.bcolors.UNDERLINE + "EMERGENCY DISABLE: THIS IS TO BE USED IN AN EMERGENCY ONLY\n(Requires Superuser permissions)" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
    if scripts.checkAPINoPrint():
        dfObj = listWAFIDsNoPrompt()
        try:
            inVar = int(input("\n\nEnter index of WAF to display [Enter to exit]: "))
            print(str(dfObj['WAF ID'].iloc[inVar]))
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.strip(' ').lower() == 'e':
                scripts.clear()
                scripts.WAFMenu()
            scripts.clear()
            disableWAF()
        print(scripts.bcolors.WARNING + scripts.bcolors.UNDERLINE + "EMERGENCY DISABLE: THIS IS TO BE USED IN AN EMERGENCY ONLY" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        while "Not a valid response.":
            reply = str(input("Request: https://api.fastly.com/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/disable\nCorrect service " + str(dfObj['Name'].iloc[inVar]) + " [Y/n]: ")).lower().strip()
            if reply[0] == 'y':
                break
            if reply[0] == 'n':
                scripts.clear()
                disableWAF()
                break
        header={"Accept":"application/vnd.api+json"}
        header.update({"Content-Type":"application/vnd.api+json"})
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.patch("https://api.fastly.com/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/disable",headers=header)
        if r.status_code == 202:
            print(scripts.bcolors.OKGREEN + "Disabled WAF" + scripts.bcolors.ENDC)
            pprint.pprint(r.json()['data'])
            input("Press ENTER to return to menu...")
        else:
            input(scripts.bcolors.WARNING + "Error with request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def enableWAF():
    print(scripts.bcolors.WARNING + scripts.bcolors.UNDERLINE + "EMERGENCY ENABLE: THIS IS TO BE USED IN AN EMERGENCY ONLY (only works on emergency disabled WAF)\n(Requires Superuser permissions)" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
    if scripts.checkAPINoPrint():
        dfObj = listWAFIDsNoPrompt()
        try:
            inVar = int(input("\n\nEnter index of WAF to display: "))
            str(dfObj['WAF ID'].iloc[inVar])
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.strip(' ').lower() == 'e':
                scripts.clear()
                scripts.WAFMenu()
            scripts.clear()
            enableWAF()
        header={"Accept":"application/vnd.api+json"}
        header.update({"Content-Type":"application/vnd.api+json"})
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.patch("https://api.fastly.com/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/enable",headers=header)
        if r.status_code == 202:
            print(scripts.bcolors.OKGREEN + "Enabled WAF" + scripts.bcolors.ENDC)
            pprint.pprint(r.json()['data'])
            input("Press ENTER to return to menu...")
        else:
            input(scripts.bcolors.WARNING + "Error with request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)