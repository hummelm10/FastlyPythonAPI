import requests
import scripts
import pprint
import pandas
from pandas.io.json import json_normalize

def activateLoop(dfObj):
    try:
        inVar = int(input("\n\nEnter index of service to view details/activate: "))
        print(str(dfObj['Name'].iloc[inVar]))
        print(str(dfObj['ID'].iloc[inVar]))
    except:
        e = input("Not a valid number. Press enter to continue or E to exit...")
        if e.lower() == 'e':
            return
        scripts.clear()
        print(dfObj)
        activateLoop(dfObj)
    header={"Accept":"application/json"}
    header.update({"Fastly-Key":scripts.getKeyFromConfig()})
    r=requests.get("https://api.fastly.com/service/" + str(dfObj['ID'].iloc[inVar]) + "/details",headers=header)
    if r.status_code == 401:
        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    elif r.status_code == 200:
        services = r.json()
        # pprint.pprint(services['versions'])
        with scripts.DataFrameFromDict(services['versions']) as df2:
            df2['Version'] = df2['number']
            df2['Created On'] = df2['created_at']
            df2['Updated On'] = df2['updated_at']
            df2['Locked'] = df2['locked']
            df2['Staging'] = df2['staging']
            df2['Testing'] = df2['testing']
            df2['Comment'] = df2['comment']
    print("Active/Deployed Version: " + str(services['active_version']['number']))
    print(df2.to_string(index=False)) 
    try:
        inVar2 = int(input("Enter version of service to activate: "))
        print("https://api.fastly.com/service/" + str(dfObj['ID'].iloc[inVar]) + "/version/" + str(inVar2) + "/activate")
    except:
        e = input("Not a valid number. Press enter to continue or E to exit...")
        if e.lower() == 'e':
            return
        scripts.clear()
        activateLoop(dfObj)
    header={"Accept":"application/vnd.api+json"}
    header.update({"Fastly-Key":scripts.getKeyFromConfig()})
    while "Not a valid response.":
        reply = str(input("Correct service [Y/n]: ")).lower().strip()
        if reply == 'y':
            r=requests.put("https://api.fastly.com/service/" + str(dfObj['ID'].iloc[inVar]) + "/version/" + str(inVar2) + "/activate",headers=header)
            break
        if reply == 'n':
            scripts.clear()
            print(dfObj)
            activateLoop(dfObj)
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
                print(dfObj)
                activateLoop(dfObj)
            if reply == 'n':
                scripts.WAFMenu()
    else:
        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    return

def activateService():
    if scripts.checkAPINoPrint():
        dfObj = scripts.listServicesNoPrint()
        print(dfObj)
        activateLoop(dfObj)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)