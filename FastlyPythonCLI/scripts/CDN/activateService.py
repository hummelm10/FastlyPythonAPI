import requests
import scripts
import pprint

def activateService():
    if scripts.checkAPINoPrint():
        dfObj = scripts.listServicesNoPrint()
        print(dfObj)
        try:
            inVar = int(input("\n\nEnter index of service to activate: "))
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.lower() == 'e':
                return
            scripts.clear()
            activateService()
        try:
            inVar2 = int(input("Enter version of service to activate: "))
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.lower() == 'e':
                return
            scripts.clear()
            activateService()
        header={"Accept":"application/vnd.api+json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        print("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/version/" + str(inVar2) + "/activate")
        while "Not a valid response.":
            reply = str(input("Correct service [Y/n]: ")).lower().strip()
            if reply == 'y':
                r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/version/" + str(inVar2) + "/activate",headers=header)
            if reply == 'n':
                scripts.clear()
                activateService()
                break
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 404:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            pprint.pprint(r.json())
            while "Not a valid response.":
                reply = str(input("Activate another service [Y/n]: ")).lower().strip()
                if reply == 'y':
                    scripts.clear()
                    activateService()
                if reply == 'n':
                    break
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)