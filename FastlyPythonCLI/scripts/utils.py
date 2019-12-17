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

def mainMenu():
    while True:
        scripts.clear()
        #Display menu options 
        print(' ' + scripts.bcolors.BOLD + scripts.bcolors.UNDERLINE + scripts.bcolors.HEADER + 'MAIN MENU' + \
            scripts.bcolors.ENDC + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print('1: WAF')
        print('2: CDN')
        print('3: List Services')
        print('4: Check API Key')
        print('5: Generate API Key')
        print('6: List API Keys')
        print('0: Revoke API Key')
        print('Q to quit')
        print(scripts.bcolors.HEADER + '===========' + scripts.bcolors.ENDC)
        print(' ')
        choice = input('Option: ')     #get user's choice

        if choice == '1':
            scripts.clear()
            scripts.WAFMenu()
        elif choice == '2':
            scripts.clear()
            scripts.CDNMenu()
        elif choice == '3':
            scripts.clear()
            scripts.listServices()
        elif choice == '4':
            scripts.clear()
            scripts.checkAPI()
        elif choice == '5':
            scripts.clear()
            scripts.generateKey()    
        elif choice == '6':
            scripts.clear()
            scripts.getAllTokens()
        elif choice == '0':
            scripts.clear()
            scripts.revokeKey()
        elif choice == 'Q' or choice == 'q':
            exit()
        else:
            input('Not a valid choice. Hit enter to continue...')

def getServicesObj():
    if scripts.checkAPINoPrint():
        print("This may take a while. Enumerating services...")
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
                        df.at[x,'Domain(s)'] = ", ".join(returnlist)
            return df
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)

def getDetails(df):
    pandas.set_option('display.max_colwidth', -1)
    print(scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "FASTLY SERVICES" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
    print(df)
    try:
        inVar = int(input("\n\nEnter index of service to view details: "))
        print(str(df['Name'].iloc[inVar]))
        print(str(df['ID'].iloc[inVar]))
    except:
        e = input("Not a valid number. Press enter to continue or E to exit...")
        if e.lower() == 'e':
            clear()
            mainMenu()
    header={"Accept":"application/json"}
    header.update({"Fastly-Key":scripts.getKeyFromConfig()})
    r=requests.get("https://api.fastly.com/service/" + str(df['ID'].iloc[inVar]) + "/details",headers=header)
    if r.status_code == 401:
        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    elif r.status_code == 200:
        services = r.json()
        # pprint.pprint(services['versions'])
        print("Active/Deployed Version: " + str(services['active_version']['number']))
        with DataFrameFromDict(services['versions']) as df2:
            df2['Version'] = df2['number']
            df2['Created On'] = df2['created_at']
            df2['Updated On'] = df2['updated_at']
            df2['Locked'] = df2['locked']
            df2['Staging'] = df2['staging']
            df2['Testing'] = df2['testing']
            df2['Comment'] = df2['comment']
    print(df2.to_string(index=False))
    while "Not a valid response.":
        reply = str(input("View another service [Y/n]: ")).lower().strip()
        if reply == 'y':
            clear()
            getDetails(df)
        if reply == 'n':
            mainMenu()

def listServices():
    df = getServicesObj()
    getDetails(df)

def listServicesNoPrint():
    if scripts.checkAPINoPrint():
        print("This may take a while. Enumerating services...")
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