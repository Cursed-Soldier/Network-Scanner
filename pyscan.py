import os
import sys
import subprocess
import argparse

def Ping(ip):
    response = os.system("ping -c1 -W 1 " + str(ip))
    if(response == 0):
        #Host is up
        return True

    else:
        #Host is down
        return False


def Nmap(ipList, stage, verbose):
    results = []

    if(stage == 1):
        print("Scanning ports 80 and 443...")
        #Do a port 80,443 scan
        results.clear()
        
        command = ["sudo", "nmap", "-sS", "-p80,443", "--open", "-oG", "-"]
        for i in range(len(ipList)):
            newCommand = command
            newCommand.append(ipList[i])
            if(verbose):
                print("NMAP " + ipList[i])
            if i == (len(ipList )- 1):
                results = NmapScan(newCommand)
            else:
                NmapScan(newCommand)
                          

    elif(stage == 2):
        print("Scanning top 1000 ports...")
        #Do a top 1000 ports scan
        results.clear()

        command = ["sudo", "nmap", "-sS", "--top-ports", "1000", "--open", "-oG", "-"]
        for i in range(len(ipList)):
            newCommand = command
            newCommand.append(ipList[i])
            if(verbose):
                print("NMAP " + ipList[i])
            if i == (len(ipList )- 1):
                results = NmapScan(newCommand)
            else:
                NmapScan(newCommand)

    elif(stage == 3):
        print("Scanning all 65525 ports...")
        #Do a full ports scan
        results.clear()

        command = ["sudo", "nmap", "-sS", "-p0-65535", "--open", "-oG", "-"]
        for i in range(len(ipList)):
            newCommand = command
            newCommand.append(ipList[i])
            if(verbose):
                print("NMAP " + ipList[i])
            if i == (len(ipList )- 1):
                results = NmapScan(newCommand)
            else:
                NmapScan(newCommand)        

    return results          


def NmapScan(command):
    assets = []
    
    scan = subprocess.Popen(command, stdout=subprocess.PIPE)
    for output in scan.stdout:
        line = str(output).split(" ")
        if("Up\\n'" in line):
            assets.append(line[1])

    return assets



def Scan(stage, filename, datafile, verbose):
    if(verbose):
        print("Starting NMAP scan...")
    #Run nmap on command specified
    ipLog = Nmap(ips,stage,verbose)

    if(len(ipLog) > 0):
        WriteFile(filename, False, ipLog)



def WriteFile(filename, ping, ipLog):
    newFile = open(filename, "w")
    for ip in ipLog:
        newFile.write(ip + "\n")
    for ip in ipLog:
        if(ping == False):
            ips.remove(ip)
    newFile.close()
    ipLog.clear()

def CreateFolder(saveFolder):
    currentDir = os.getcwd()
    path = os.path.join(currentDir, saveFolder)
    if os.path.exists(path) or os.path.isdir(path):
        os.chdir(saveFolder)
    else:
        os.mkdir(path)
        os.chdir(saveFolder)

def SetParser():
    parser.add_argument("-i", "--input", required = "true", help = "input file (.txt) with the IPs to be used in the network scan")
    parser.add_argument("-o", "--output", default = "results", help = "name of the output folder to be used (default = results)")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "verbose message option")
    parser.add_argument("-s", "--stages", default="basic", choices=["ping","basic","topports","full"], help = "scan intensity selector")




#Start of program
parser = argparse.ArgumentParser()
SetParser()
args = parser.parse_args()

                          
ips = []
ipLog = []

datafile = args.input
saveFolder = args.output
verbose = args.verbose
stages = args.stages

try:
    ipfile = open(str(datafile), "r")
    if verbose:
        print("Starting ping scan...")
    for ip in ipfile:
        ip = str(ip).strip()
        #Run ping against ips that are being onboarded
        if(Ping(ip)):
            ipLog.append(ip)

        else:
            ips.append(ip)
            
        
    ipfile.close()

    #Create output folder
    CreateFolder(saveFolder)

    #Write successful ping results to file
    WriteFile("results-ping.txt", True, ipLog)


    if(stages != "ping"):
        #Nmap ports 80,443
        Scan(1,"results-nmap1.txt", datafile, verbose)

        if(stages!= "basic"):
            #Nmap top 1000 ports
            Scan(2,"results-nmap2.txt", datafile, verbose)

            if(stages != "topports"):
                #Nmap all ports
                Scan(3,"results-nmap3.txt", datafile, verbose)

    #Write remaining 'dead' assets
    WriteFile("results-dead.txt", False, ips)

    print('''
    Scan successful, view results in the files created

    Goodbye Commander!''')

except:
    print("Could not read file provided")  

