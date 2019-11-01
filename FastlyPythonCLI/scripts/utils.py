from os import system, name
from xml.dom import minidom

# define our clear screen function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def getKeyFromConfig():
    configXML = minidom.parse('Config.xml')
    items = configXML.getElementsByTagName('item')
    return str(items[0].childNodes[0].data)

def writeKeyToXML(key):
    print("Do something here")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'