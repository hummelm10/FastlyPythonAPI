#Imports
from getpass import getpass
from .utils import clear
from .utils import writeKeyToXML
from .utils import bcolors
from xml.dom import minidom
import requests


def generateKey():
    print(bcolors.OKBLUE + 'Generating key...' + bcolors.ENDC)
    username = input("Username: ")
    password = getpass()
    OTP = input("OTP [leave blank if OTP is not enabled]: ")
    # print(username)
    # print(password)
    # print(OTP)
    header={"Accept":"application/json"}
    header.update({"Content-Type":"application/x-www-form-urlencoded"})
    data={'username':username}
    data.update({'password':password})
    if OTP != "":
        header.update({"Fastly-OTP":OTP})
    r=requests.post("https://api.fastly.com/tokens",headers=header,data=data)
    if r.status_code == 400:
        print(bcolors.WARNING + "Return Message:" + bcolors.ENDC, end =" ")
        print(r.json()['detail'])
        input('Press ENTER to continue...')
        clear()
        # generateKey()
    elif r.status_code == 200:
        accessToken = r.json()['detail']
        configXML = minidom.parse('Config.xml')
        items = configXML.getElementsByTagName('item')
        items[0].childNodes[0].data = accessToken
        F=open('Config.xml',"w")
        configXML.writexml(F)
        F.close()
        input('API Key generated and saved. Press ENTER to continue...')
    else:
        print(bcolors.WARNING + "Unknown Response: " + str(r.status_code) + bcolors.ENDC)
        input("Press ENTER to continue...")
        exit()
    return
