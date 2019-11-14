import requests
import scripts
import pprint
import pandas
from pandas.io.json import json_normalize
from .listWAFIDs import listWAFIDs
from .listWAFIDs import listWAFIDsNoPrompt
from .getRuleByID import getRuleByID
import pydoc

def OWASP():
    pandas.set_option('display.max_rows', 1000)
    if scripts.checkAPINoPrint():
        dfObj = listWAFIDsNoPrompt()
        # print(dfObj)
        try:
            inVar = int(input("\n\nEnter index of WAF to display: "))
        except:
            e = input("Not a valid number. Press enter to continue or E to exit...")
            if e.lower() == 'e':
                return
            scripts.clear()
            OWASP()
        header={"Accept":"application/vnd.api+json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/service/" + str(dfObj['Service ID'].iloc[inVar]) + "/wafs/" + str(dfObj['WAF ID'].iloc[inVar]) + "/owasp",headers=header)
        # pprint.pprint(r.json()['data'])
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 404:
            # * no waf for that service
            pass
        elif r.status_code == 200:
            with scripts.utils.DataFrameFromDict(r.json()['data']) as df:
                owaspid = str(df['id'].iloc[0])
                df['Allowed HTTP Versions'] = df['attributes.allowed_http_versions']
                df['Allowed Methods'] = df['attributes.allowed_methods']
                df['Allowed Request Content Type'] = df['attributes.allowed_request_content_type']
                df['Allowed Request Content Type Charset'] = df['attributes.allowed_request_content_type_charset']
                df['Arg Length'] = df['attributes.arg_length']
                df['Arg Namr Length'] = df['attributes.arg_name_length']
                df['Combined File Sizes'] = df['attributes.combined_file_sizes']
                df['Created At'] = df['attributes.created_at']
                df['Critical Anomaly Score'] = df['attributes.critical_anomaly_score']
                df['CRS Validate UTF8 Encoding'] = df['attributes.crs_validate_utf8_encoding']
                df['Error Anomaly Score'] = df['attributes.error_anomaly_score']
                df['High Risk Country Codes'] = df['attributes.high_risk_country_codes']
                df['HTTP Violation Score Threshold'] = df['attributes.http_violation_score_threshold']
                df['Inbound Anomaly Score Threshold'] = df['attributes.inbound_anomaly_score_threshold']
                df['LFI Score Threshold'] = df['attributes.lfi_score_threshold']
                df['Max File Size'] = df['attributes.max_file_size']
                df['Max Num Args'] = df['attributes.max_num_args']
                df['Notice Anomaly Score'] = df['attributes.notice_anomaly_score']
                df['Paranoia Level'] = df['attributes.paranoia_level']
                df['PHP Injection Score Threshold'] = df['attributes.php_injection_score_threshold']
                df['RCE Score Threshold'] = df['attributes.rce_score_threshold']
                df['Restricted Extensions'] = df['attributes.restricted_extensions']
                df['Restricted Headers'] = df['attributes.restricted_headers']
                df['RFI Score Threshold'] = df['attributes.rfi_score_threshold']
                df['Session Fixation Score Threshold'] = df['attributes.session_fixation_score_threshold']
                df['SQL Injection Score Threshold'] = df['attributes.sql_injection_score_threshold']
                df['Total Arg Length'] = df['attributes.total_arg_length']
                df['Updated At'] = df['attributes.updated_at']
                df['Warning Anomaly Score'] = df['attributes.warning_anomaly_score']
                df['XSS Score Threshold'] = df['attributes.xss_score_threshold']
            # df.insert(2, 'Severity', None)
            # df.insert(3, 'Description', None)
            # if x == 0:
            #     df_all_rows = df
            # for x in range(len(df.index)):
            #     obj = getRuleByID(str(df['ID'].iloc[x]))
            #     df.at[x,'Severity'] = obj['Severity'].iloc[0]
            #     df.at[x,'Description'] = obj['Description'].iloc[0]
            # pandas.set_option('display.max_colwidth', -1)
            # df_all_rows = df_all_rows.append(df,ignore_index = True)
            print("\n\n" + scripts.bcolors.OKBLUE + scripts.bcolors.UNDERLINE + "OWASP CONFIG for " + owaspid  + scripts.bcolors.ENDC + scripts.bcolors.ENDC)
            print(df.iloc[0])
            input("Press ENTER to return to menu...")
        else:
            input(scripts.bcolors.WARNING + "Error with services request.\nStatus: " + str(r.status_code) +  "\nPress ENTER to continue..." + scripts.bcolors.ENDC)

    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)