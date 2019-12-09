import requests
import scripts
import pandas
from pandas.io.json import json_normalize
import pydoc
import numpy

def listWAFRules():
    pandas.set_option('display.max_rows', 20000)
    if scripts.checkAPINoPrint():
        header={"Accept":"application/vnd.api+json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/wafs/rules",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            pages=int(json_normalize(r.json()['meta'])['total_pages'])
            df_all_rows = pandas.DataFrame()
            for x in range(pages):
                x+=1
                print("Parsing page " + str(x) + " of " + str(pages) + " total pages")
                r=requests.get("https://api.fastly.com/wafs/rules?page[number]=" + str(x),headers=header)
                with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                    df['ID'] = df['id']
                    df['Rule ID'] = df['attributes.rule_id']
                    df['Description'] = df['attributes.message']
                    df['Severity'] = df['attributes.severity']
                pandas.set_option('display.max_colwidth', -1)
                df_all_rows = df_all_rows.append(df, ignore_index=True)
                df_all_rows.reset_index(drop=True, inplace=True)
            filter = input("Enter filter for rules [all]: ")
            if filter != "":
                print(scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "FASTLY WAF RULES" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
                mask = df_all_rows.apply(lambda row: row.astype(str).str.contains(str(filter), case=False, na=False, regex=False).any(), axis=1)
                pydoc.pager(str(df_all_rows[mask]))
            else:
                print(scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "FASTLY WAF RULES" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
                pydoc.pager(str(df_all_rows))
            input("Press ENTER to return to menu...")
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)