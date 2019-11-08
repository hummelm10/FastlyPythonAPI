import requests
import scripts
import pandas
from pandas.io.json import json_normalize

def listWAFIDs():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        services = scripts.listServicesNoPrint()
        if services is not None:
            dfObj = pandas.DataFrame()
            for x in range(len(services.index)):
                header={"Accept":"application/vnd.api+json"}
                header.update({"Fastly-Key":scripts.getKeyFromConfig()})
                # print("https://api.fastly.com/service/" + str(services['ID'].iloc[x]) + "/version/" + str(services['Version'].iloc[x]) + "/wafs")
                r=requests.get("https://api.fastly.com/service/" + str(services['ID'].iloc[x]) + "/version/" + str(services['Version'].iloc[x]) + "/wafs",headers=header)
                if r.status_code == 401:
                    input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
                elif r.status_code == 404:
                    # * no waf for that service
                    pass    
                elif r.status_code == 200:
                    with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                        if df.empty != True:
                            df.insert(0, 'Name', str(services['Name'].iloc[x]))
                            df.insert(1, 'Service ID', str(services['ID'].iloc[x]))
                            df.insert(2, 'Domain(s)', str(services['Domain(s)'].iloc[x]))
                            df['WAF ID'] = df['id']
                            df['Version'] = df['attributes.version']
                            df['Last Push'] = df['attributes.last_push']
                            df['Logged Rules'] = df['attributes.rule_statuses_log_count']
                            df['Blocked Rules'] = df['attributes.rule_statuses_block_count']
                            df['Disabled Rules'] = df['attributes.rule_statuses_disabled_count']
                    if df.empty != True:
                        dfObj = dfObj.append(df)
                else:
                    input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
            print(dfObj)
            input("Press ENTER to continue...")
            return dfObj
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)
    return None

def listWAFIDsNoPrompt():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        services = scripts.listServicesNoPrint()
        if services is not None:
            dfObj = pandas.DataFrame()
            for x in range(len(services.index)):
                if not services['Version'].isnull().iloc[x]:
                    header={"Accept":"application/vnd.api+json"}
                    header.update({"Fastly-Key":scripts.getKeyFromConfig()})
                    # print("https://api.fastly.com/service/" + str(services['ID'].iloc[x]) + "/version/" + str(services['Version'].iloc[x]) + "/wafs")
                    r=requests.get("https://api.fastly.com/service/" + str(services['ID'].iloc[x]) + "/version/" + str(services['Version'].iloc[x]) + "/wafs",headers=header)
                    if r.status_code == 401:
                        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
                    elif r.status_code == 404:
                        # * no waf for that service
                        pass
                    elif r.status_code == 200:
                        with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                            if df.empty != True:
                                df.insert(0, 'Name', str(services['Name'].iloc[x]))
                                df.insert(1, 'Service ID', str(services['ID'].iloc[x]))
                                df.insert(2, 'Domain(s)', str(services['Domain(s)'].iloc[x]))
                                df['WAF ID'] = df['id']
                                df['Version'] = df['attributes.version']
                                df['Last Push'] = df['attributes.last_push']
                                df['Logged Rules'] = df['attributes.rule_statuses_log_count']
                                df['Blocked Rules'] = df['attributes.rule_statuses_block_count']
                                df['Disabled Rules'] = df['attributes.rule_statuses_disabled_count']
                        if df.empty != True:
                            dfObj = dfObj.append(df)
                    else:
                        input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
            print(dfObj)
            return dfObj
        else:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)
    return None