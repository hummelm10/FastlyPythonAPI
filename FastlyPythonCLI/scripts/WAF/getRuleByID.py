import requests
import scripts
import pprint
import pandas
from pandas.io.json import json_normalize
from .listWAFIDs import listWAFIDs
from .listWAFIDs import listWAFIDsNoPrompt

def getRuleByID(ruleid):
    header={"Accept":"application/vnd.api+json"}
    header.update({"Fastly-Key":scripts.getKeyFromConfig()})
    r=requests.get("https://api.fastly.com/wafs/rules/" + ruleid,headers=header)
    if r.status_code == 401:
        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    elif r.status_code == 200:
        with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
            df['ID'] = df['id']
            df['Rule ID'] = df['attributes.rule_id']
            df['Description'] = df['attributes.message']
            df['Severity'] = df['attributes.severity']
        # print(df)
        return df
    else:
        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)