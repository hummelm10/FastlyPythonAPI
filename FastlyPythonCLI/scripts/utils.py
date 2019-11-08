from os import system, name
from xml.dom import minidom
import scripts
import requests
import pandas
from pandas.io.json import json_normalize
import pprint

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
        r=requests.get("https://api.fastly.com/service",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            services = r.json()
            with DataFrameFromDict(services) as df:
                df['ID'] = df['id']
                df['Name'] = df['name']
                df['Version'] = df['version']
            df.insert(3, 'Domain(s)', None)
            # print(df)
            for x in range(len(df.index)):
                if not df['Version'].isnull().iloc[x]:
                    id = str(df['ID'].iloc[x])
                    # print("https://api.fastly.com/service/" + id + "/domain")
                    r2=requests.get("https://api.fastly.com/service/" + id + "/domain",headers=header)
                    # pprint.pprint(r2.json())
                    returns=json_normalize(r2.json())
                    if r2.json():
                        returnlist = returns['name'].tolist()
                        df.at[x,'Domain(s)'] =", ".join(returnlist)
            pandas.set_option('display.max_colwidth', -1)
            print(df)
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def listServicesNoPrint():
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/service",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            services = r.json()
            with DataFrameFromDict(services) as df:
                df['ID'] = df['id']
                df['Name'] = df['name']
                df['Version'] = df['version']
            df.insert(3, 'Domain(s)', None)
            # print(df)
            for x in range(len(df.index)):
                if not df['Version'].isnull().iloc[x]:
                    id = str(df['ID'].iloc[x])
                    # print("https://api.fastly.com/service/" + id + "/domain")
                    r2=requests.get("https://api.fastly.com/service/" + id + "/domain",headers=header)
                    # pprint.pprint(r2.json())
                    returns=json_normalize(r2.json())
                    if r2.json():
                        returnlist = returns['name'].tolist()
                        df.at[x,'Domain(s)'] =", ".join(returnlist)
            pandas.set_option('display.max_colwidth', -1)
            return df
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)