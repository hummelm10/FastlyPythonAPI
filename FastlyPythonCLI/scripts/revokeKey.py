import requests
import pandas
from .utils import bcolors
from .utils import clear
from .utils import getKeyFromConfig
from .getAllTokens import getAllTokens

def revokeKey():
    df = getAllTokens(False)
    try:
        revokeTokenIndex = int(input("Enter index of token to revoke: "))
        revokeTokenID = df['ID'].iloc[revokeTokenIndex]
    except:
        input("Not a valid number. Press enter to continue...")
        clear()
        revokeKey()
    header={"Accept":"application/json"}
    header.update({"Fastly-Key":getKeyFromConfig()})
    # print(df)
    # print(str(revokeTokenID))
    r=requests.delete("https://api.fastly.com/tokens/"+str(revokeTokenID),headers=header)
    if r.status_code == 401:
        print(bcolors.WARNING + "Return Message:" + bcolors.ENDC, end =" ")
        print(r.json()['msg'])
        input('Press ENTER to continue...')
        clear()
    elif r.status_code == 204:
        print("Revoked Token " + str(revokeTokenID))
        input("Press ENTER to continue...")
    else:
        print(bcolors.WARNING + "Unknown Response: " + str(r.status_code) + bcolors.ENDC)
        input("Press ENTER to continue...")
        exit()
    return