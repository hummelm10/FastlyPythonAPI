#Imports
from xml.dom import minidom
from .generateKey import generateKey
from .utils import clear
from .utils import getKeyFromConfig
from .utils import bcolors
import requests
import os.path
from os import path

def checkAPI():
    if path.exists("Config.xml") == False:
        print(bcolors.FAIL + "Config.xml file is missing. Exiting Application." + bcolors.ENDC)
        exit()
    print('Getting current API key information...')
    print(bcolors.OKBLUE + "API Key: " + bcolors.ENDC + getKeyFromConfig())
    header={"Accept":"application/json"}
    header.update({"Fastly-Key":getKeyFromConfig()})
    r=requests.get("https://api.fastly.com/tokens/self",headers=header)
    if r.status_code == 401:
        print(bcolors.WARNING + "Return Message:" + bcolors.ENDC, end =" ")
        print(r.json()['msg'])
        input('Press ENTER to generate key...')
        clear()
        generateKey()
    elif r.status_code == 200:
        input("API Key appears valid. Press ENTER to continue...")
    else:
        print(bcolors.WARNING + "Unknown Response: " + str(r.status_code) + bcolors.ENDC)
        input("Press ENTER to continue...")
        exit()
    return

def checkAPINoPrint():
    header={"Accept":"application/json"}
    header.update({"Fastly-Key":getKeyFromConfig()})
    r=requests.get("https://api.fastly.com/tokens/self",headers=header)
    if r.status_code == 401:
        return False
    elif r.status_code == 200:
        return True
    else:
        return False