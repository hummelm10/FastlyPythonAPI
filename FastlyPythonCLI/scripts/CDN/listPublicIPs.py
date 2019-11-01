import requests
import scripts

def listPublicIPs():
    if scripts.checkAPINoPrint():
        header={"Accept":"application/json"}
        header.update({"Fastly-Key":scripts.getKeyFromConfig()})
        r=requests.get("https://api.fastly.com/tokens/self",headers=header)
        if r.status_code == 401:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
        elif r.status_code == 200:
            print(r.json())
            input("Press ENTER to continue...")
        else:
            input(scripts.bcolors.WARNING + "Error with request. Press ENTER to continue..." + scripts.bcolors.ENDC)
    else:
        input(scripts.bcolors.WARNING + "Error with API Key, generate a new one. Press ENTER to continue..." + scripts.bcolors.ENDC)