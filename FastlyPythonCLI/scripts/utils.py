from os import system, name
from xml.dom import minidom
import scripts
import requests
import pandas
from pandas.io.json import json_normalize

class DataFrameFromDict(object):
    def __init__(self, data):
        self.df = json_normalize(data)
        self.columns = list(self.df.columns.values)    
    def __enter__(self):
        return self.df    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.df.drop([c for c in self.columns], axis=1, inplace=True)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# define our clear screen function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def getKeyFromConfig():
    configXML = minidom.parse('Config.xml')
    items = configXML.getElementsByTagName('item')
    return str(items[0].childNodes[0].data)

def writeKeyToXML(key):
    print("Do something here")

def listServices():
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/services",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            services = r.json()['data']
            with DataFrameFromDict(services) as df:
                df['ID'] = df['id']
                df['Name'] = df['attributes.name']
                df['Version'] = df['attributes.active_version']
            print(df)
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def listServicesNoPrint():
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/services",headers=header)
        if r.status_code == 401:
            return None
        elif r.status_code == 200:
            services = r.json()['data']
            with DataFrameFromDict(services) as df:
                df['ID'] = df['id']
                df['Name'] = df['attributes.name']
                df['Version'] = df['attributes.active_version']
            return df
        else:
            return None
    else:
        return None

