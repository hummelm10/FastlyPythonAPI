import requests
import scripts
import pprint
import pandas
import json
from pandas.io.json import json_normalize
from .listWAFIDs import listWAFIDs
from .listWAFIDs import listWAFIDsNoPrompt
from .getRuleByID import getRuleByID
import pydoc

def getWAFRuleset():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        dfObj = listWAFIDsNoPrompt()
        # print(dfObj)
        try:
            inVar = int(input("\n\nEnter index of WAF to display: "))
            print("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rule_statuses")
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.lower() == 'e':
                return
            scripts.clear()
            getWAFRuleset()
        header={"Accept":"application/vnd.api+json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        # input("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/ruleset")
        r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rule_statuses",headers=header)
        pages=int(json_normalize(r.json()['meta'])['total_pages'])
        df_all_rows = pandas.DataFrame()
        for x in range(pages):
            x+=1
            print("Parsing page " + str(x) + " of " + str(pages) + " total pages")
            r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rule_statuses?page[number]=" + str(x),headers=header)
            if r.status_code == 401:
                input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
            elif r.status_code == 404:
                # * no waf for that service
                pass
            elif r.status_code == 200:
                with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                    df['Rule ID'] = df['id']
                    df['Num ID'] = df['attributes.modsec_rule_id']
                    df['ID'] = df['attributes.unique_rule_id']
                    df['Status'] = df['attributes.status']
                df.insert(2, 'Severity', None)
                df.insert(3, 'Description', None)
                if x == 0:
                    df_all_rows = df
                for x in range(len(df.index)):
                    obj = getRuleByID(str(df['ID'].iloc[x]))
                    df.at[x,'Severity'] = obj['Severity'].iloc[0]
                    df.at[x,'Description'] = obj['Description'].iloc[0]
                pandas.set_option('display.max_colwidth', -1)
                df_all_rows = df_all_rows.append(df,ignore_index = True)
                df_all_rows.reset_index()
            else:
                input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
                break
        filter = input("Enter filter for rules [all]: ")
        if filter != "":
            try:
                mask = df_all_rows.apply(lambda row: row.astype(int).str.contains(int(filter), case=False, na=False, regex=False).any(), axis=1)
                print(scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "FASTLY WAF RULES" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
                pydoc.pager(str(df_all_rows[mask]))
            except:
                mask = df_all_rows.apply(lambda row: row.astype(str).str.contains(str(filter), case=False, na=False, regex=False).any(), axis=1)
                print(scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "FASTLY WAF RULES" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
                pydoc.pager(str(df_all_rows[mask]))
        else:
            print(scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "FASTLY WAF RULES" + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
            pydoc.pager(str(df_all_rows))
        while "Not a valid response.":
            reply = str(input("Modify filtered rules [Y/n]: ")).lower().strip()
            if reply == 'y':
                action = str(input("Enter action to perform on rules (disabled, log, block):")).lower().strip()
                body = {}
                datatemp = {}
                attributes = {}
                dfFiltered = df_all_rows[mask]
                for index, row in dfFiltered.iterrows():
                    print(str(row['Rule ID']))
                    datatemp.update({"id":str(row['Rule ID'])})
                    datatemp.update({"type":"rule_status"})
                    attributes.update({"status":action})
                    datatemp.update({"attributes":attributes})
                    body.update({"data":datatemp})
                    #print(json.dumps(data))
                    header={"Accept":"application/vnd.api+json"}
                    header.update({"Fastly-Key":scripts.getKeyFromConfig()})
                   
                    #r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rules/" + str(rid) + "/rule_status",headers=header)
                    #pprint.pprint(r.json()['data'])
                    header.update({"Content-Type":"application/vnd.api+json"})
                    #print(json.dumps(header))
                    #print(json.dumps(body))
                    #print("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rules/" + str(row['Num ID']) + "/rule_status")
                    r=requests.patch("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rules/" + str(row['Num ID']) + "/rule_status", data=str(json.dumps(body)) ,headers=header)
                    if r.status_code == 200:
                        pprint.pprint(r.json()['data'])
                    else:
                        print(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) + scripts.bcolors.ENDC)
                break
            if reply == 'n':
                scripts.WAFMenu()
        input("Press ENTER to continue...")
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)