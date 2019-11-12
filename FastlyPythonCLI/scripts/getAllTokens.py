#custom
from .generateKey import generateKey
from .utils import clear
from .utils import getKeyFromConfig

#custom classes
from .utils import bcolors
from .utils import DataFrameFromDict

#Python packages
from xml.dom import minidom
import requests
import pandas
from pandas.io.json import json_normalize


def getAllTokens(printInput=True):
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
        with DataFrameFromDict(r.json()) as df:
            df['ID'] = df['id']
            df['User ID'] = df['user_id']
            df['Customer ID'] = df['customer_id']
            df['Name'] = df['name']
            df['Scope'] = df['scope']
            df['Last Used At'] = df['last_used_at']
            df['Expiration'] = df['expires_at']
            df['IP'] = df['ip']
        print(df)
        if printInput:
            input("Press ENTER to continue...")
        else:
            return df
    else:
        print(bcolors.WARNING + "Unknown Response: " + str(r.status_code) + bcolors.ENDC)
        input("Press ENTER to continue...")
        exit()
    return