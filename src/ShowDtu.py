# Build exe with: pyinstaller ShowDtu.py --onefile

import subprocess
import webbrowser
import urllib.request

debug   = 0 # set debug flag to 1 to print als log messages with LogMsg()
testing = 0 # set testing flag, when the DTU is not available in the network

def getLocalIPs():
    # Get all IP adresses in network through Address Resolution Protocol
    allIp = subprocess.check_output(("arp", "-a"))
    LogMsg(allIp)
    allIpStr = str(allIp)
    LogMsg(allIpStr)
    allIpStrSplit = allIpStr.split(" ")
    LogMsg(allIpStrSplit)
    count = 0
    localIP = []
    for item in allIpStrSplit:
        count += 1
        # filter for Ip Adresses starting with 192.168
        if item.startswith('192.168.'):
            localIP.append(item)
            # print("Item nr" + str(count) + ": " + item)
            LogMsg("Local IP:" , localIP)
    return localIP

def isDtu(IP):
    DtuLink = "http://" + IP + "/api" # With the link to DTU live view the http response was fine for the router
    LogMsg(DtuLink)
    targetstr = str('192.168.0.133')

    try:
        if (IP == targetstr) and testing:
            response = urllib.request.urlopen("https://www.python.org/")
        else:
            response = urllib.request.urlopen(DtuLink)

        LogMsg("Repsonse from urllib :", response.status)
        if response.status == 200:
            return True
        else:
            return False
    except:
        LogMsg ("URL not found")
        return False

def getDtuIP(IP_ADRESS):
    # check for Dtu response
    LogMsg("IP_ADRESS: " , IP_ADRESS)
    for IP in IP_ADRESS:
        LogMsg(IP)
        routerIP = '192.168.2.1'
        if isDtu(IP) and (IP != routerIP):
            return IP
            break
    return "DTU konnte nicht gefunden werden"

def openDtuLiveView(IP):
    DtuLink = 'http://' + IP + '/live?v=0.6.9'
    LogMsg(DtuLink)
    webbrowser.open(DtuLink)  # Go to DtuWebsite

def LogMsg(*argv):
    if debug == 1:
        print(*argv)

def main():
    IP = getLocalIPs()
    LogMsg("Local IP MAIN:", IP)
    DtuIP = getDtuIP(IP)
    print("DTU IP lautet:", DtuIP)
    openDtuLiveView(DtuIP)

if __name__ == "__main__":
    main()