# Build exe with: pyinstaller ShowDtu.py --onefile

import webbrowser
import urllib.request

debug   = 0 # set debug flag to 1 to print als log messages with LogMsg()
testing = 0 # set testing flag, when the DTU is not available in the network

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

def getDtuIP():
    for IpEnding in range(100, 199):
        IP = '192.168.2.' + str(IpEnding)
        print("Check " + IP)
        if isDtu(IP):
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
    DtuIP = getDtuIP()
    print("DTU IP lautet:", DtuIP)
    openDtuLiveView(DtuIP)

if __name__ == "__main__":
    main()