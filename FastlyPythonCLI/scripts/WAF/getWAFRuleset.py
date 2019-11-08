import requests
import scripts
import pprint
import pandas
from pandas.io.json import json_normalize
from .listWAFIDs import listWAFIDs
from .listWAFIDs import listWAFIDsNoPrompt
from .getRuleByID import getRuleByID

def getWAFRuleset():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        dfObj = listWAFIDsNoPrompt()
        # print(dfObj)
        try:
            inVar = int(input("\n\nPlease select which WAF to display: "))
        except:
            input("Not a valid number. Press enter to continue...")
            scripts.clear()
            getWAFRuleset()
        header={"Accept":"application/vnd.api+json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        # input("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/ruleset")
        r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rule_statuses",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 404:
            # * no waf for that service
            pass
        elif r.status_code == 200:
            with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                df['ID'] = df['attributes.unique_rule_id']
                df['Status'] = df['attributes.status']
                # df['Rule ID'] = df['rule.data.id']
                # df['Type'] = df['rule.data.type']
            df.insert(2, 'Severity', None)
            df.insert(3, 'Description', None)
            for x in range(len(df.index)):
                obj = getRuleByID(str(df['ID'].iloc[x]))
                #print(obj)
                df.at[x,'Severity'] = obj['Severity'].iloc[0]
                df.at[x,'Description'] = obj['Description'].iloc[0]
            pandas.set_option('display.max_colwidth', -1)
            print(df)
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)