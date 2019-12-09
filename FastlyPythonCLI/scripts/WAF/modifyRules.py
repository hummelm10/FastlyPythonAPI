import requests
import scripts
import pprint
import pandas
import json
from pandas.io.json import json_normalize

def modifyRules():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        dfObj = scripts.WAF.listWAFIDsNoPrompt()
        # print(dfObj)
        try:
            inVar = int(input("\n\nEnter index of WAF to modify: "))
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.lower() == 'e':
                return
            scripts.clear()
            modifyRules()
        ruleids = str(input("Enter rule ID's to modify (Example: 1010010,931100,931110): ")).lower().strip()
        action = str(input("Enter action to perform on rules (disabled, log, block):")).lower().strip()
        ruleList = ruleids.split(",")
        data = {}
        datatemp = {}
        attributes = {}
        for rid in ruleList:
            wrid=str(dfObj['WAF ID'].iloc[inVar]) + "-" + str(rid)
            datatemp.update({"id":wrid})
            datatemp.update({"type":"rule_status"})
            attributes.update({"status":action})
            datatemp.update({"attributes":attributes})
            data.update({"data":datatemp})
            #print(json.dumps(data))
            header={"Accept":"application/vnd.api+json"}
            header.update({"Fastly-Key":scripts.getKeyFromConfig()})
            #r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rules/" + str(rid) + "/rule_status",headers=header)
            #pprint.pprint(r.json()['data'])
            header.update({"Content-Type":"application/vnd.api+json"})
            #print("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rules/" + str(rid) + "/rule_status")
            r=requests.patch("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/rules/" + str(rid) + "/rule_status", data=data ,headers=header)
            if r.status_code == 200:
                pprint.pprint(r.json()['data'])
            else:
                print(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) + scripts.bcolors.ENDC)
                break
        while "Not a valid response.":
            reply = str(input("Modify another set [Y/n]: ")).lower().strip()
            if reply == 'y':
                modifyRules()
            if reply == 'n':
                scripts.WAFMenu()
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)