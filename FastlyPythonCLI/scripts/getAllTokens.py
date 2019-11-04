from xml.dom import minidom
from .generateKey import generateKey
from .utils import clear
from .utils import getKeyFromConfig
from .utils import bcolors
import requests
import pprint


def getAllTokens():
    print('Getting all current tokens...')
    print("API Key: " + getKeyFromConfig())
    header={"Accept":"application/json"}
    header.update({"Fastly-Key":getKeyFromConfig()})
    r=requests.get("https://api.fastly.com/tokens",headers=header)
    if r.status_code == 401:
        print(bcolors.WARNING + "Return Message:" + bcolors.ENDC, end =" ")
        print(r.json()['msg'])
        input('Press ENTER to continue...')
        clear()
    elif r.status_code == 200:
        pprint.pprint(r.json())
        input("Press ENTER to continue...")
    else:
        print(bcolors.WARNING + "Unknown Response: " + r.status_code + bcolors.ENDC)
        input("Press ENTER to continue...")
        exit()
    return