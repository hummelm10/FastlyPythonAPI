import requests
import scripts
import pandas
from pandas.io.json import json_normalize

def listWAFRules():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        header={"Accept":"application/vnd.api+json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/wafs/rules",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                df['ID'] = df['id']
                df['Rule ID'] = df['attributes.rule_id']
                df['Description'] = df['attributes.message']
                df['Severity'] = df['attributes.severity']
            pandas.set_option('display.max_colwidth', -1)
            print(df)
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)