import os
import sys
import subprocess

def Ping(ip):
    response = os.system("ping -c1 -W 1 " + str(ip))
    if(response == 0):
        #Host is up
        return True

    else:
        #Host is down
        return False


def Nmap(ipList, stage):
    results = []

    if(stage == 1):
        print("Scanning ports 80 and 443...")
        #Do a port 80,443 scan
        results.clear()
        
        command = ["sudo", "nmap", "-sS", "-p80,443", "--open", "-oG", "-"]
        command = FormatCommand(command, ipList)

        results = NmapScan(command)                 

    elif(stage == 2):
        print("Scanning top 1000 ports...")
        #Do a top 1000 ports scan
        results.clear()

        command = ["sudo", "nmap", "-sS", "--top-ports", "1000", "--open", "-oG", "-"]
        command = FormatCommand(command, ipList)

        results = NmapScan(command)

    elif(stage == 3):
        print("Scanning all 65525 ports...")
        #Do a full ports scan
        results.clear()

        command = ["sudo", "nmap", "-sS", "-p0-65535", "--open", "-oG", "-"]
        command = FormatCommand(command, ipList)

        results = NmapScan(command)
        

    return results


def FormatCommand(command, ipList):
    for ip in ipList:
        command.append(ip)
        
    return command
    


def NmapScan(command):
    assets = []
    
    scan = subprocess.Popen(command, stdout=subprocess.PIPE)
    for output in scan.stdout:
        line = str(output).split(" ")
        if("Up\\n'" in line):
            assets.append(line[1])

    return assets



def Scan(stage, filename, datafile):
    print("Nmap Stage: ",stage)
    #Run nmap on command specified
    ipLog = Nmap(ips,stage)

    if(len(ipLog) > 0):
        WriteFile(filename, False, ipLog)



def WriteFile(filename, ping, ipLog):
    newFile = open(filename, "w")
    for ip in ipLog:
        newFile.write(ip + "\n")
        if(ping == False):
            ips.remove(ip)
    newFile.close()
    ipLog.clear()

def CreateFolder():
    currentDir = os.getcwd()
    path = os.path.join(currentDir, "results")
    if os.path.exists(path) or os.path.isdir(path):
        os.chdir('results')
    else:
        os.mkdir(path)
        os.chdir('results')


                          
ips = []
ipLog = []
datafile = sys.argv[1]

if(len(sys.argv) < 2 or len(sys.argv) > 2):
    print("Invalid input, provide only one input argument")

else:

    #try:

    
    
    ipfile = open(str(datafile), "r")

    for ip in ipfile:
        ip = str(ip).strip()
        #Run ping against ips that are being onboarded
        if(Ping(ip)):
            ipLog.append(ip)

        else:
            ips.append(ip)
            
        
    ipfile.close()

    #Create output folder
    CreateFolder()

    #Write successful ping results to file
    WriteFile("results-ping.txt", True, ipLog)


    #Nmap ports 80,443
    Scan(1,"results-nmap1.txt", datafile)

    #Nmap top 1000 ports
    Scan(2,"results-nmap2.txt", datafile)

    #Nmap all ports
    Scan(3,"results-nmap3.txt", datafile)

    #Write remaining 'dead' assets
    WriteFile("results-dead.txt", False, ips)
    
    print('''
Scan successful, view results in the files created

Goodbye!''')

    #except:
    #    print("Could not read file provided")  

