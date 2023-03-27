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

def NmapPing(file, verbose):
    results = []
    
    print("Running ping scan")
    results.clear()
    
    command = ["sudo", "nmap", "-iL", file, "-sn", "--open", "-oG", "-"]
    results = NmapScan(command)

    return results


def Nmap(file, stage, verbose):
    results = []

    if(stage == 1):
        print("Scanning ports 80 and 443...")
        #Do a port 80,443 scan
        results.clear()
        
        command = ["sudo", "nmap", "-sS", "-p80,443", "--open", "-oG", "-", "-iL", file]
        results = NmapScan(command)
                          

    elif(stage == 2):
        print("Scanning top 1000 ports...")
        #Do a top 1000 ports scan
        results.clear()

        command = ["sudo", "nmap", "-sS", "--top-ports", "1000", "--open", "-oG", "-", "-iL", file]
        results = NmapScan(command)

    elif(stage == 3):
        print("Scanning all 65525 ports...")
        #Do a full ports scan
        results.clear()

        command = ["sudo", "nmap", "-sS", "-p0-65535", "--open", "-oG", "-", "-iL", file]
        results = NmapScan(command)


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
    foundIps= Nmap(datafile,stage,verbose)
    return foundIps




def WriteFiles(filename, dead):
    if not dead:
        with open(filename,"w") as newFile:
            for ip in ipLog:
                newFile.write(ip.strip() + "\n")
        for ip in ipLog:
            ips.remove(ip)

    with open("results-dead.txt","w") as deadFile:
        for asset in ips:
            deadFile.write(asset.strip() + "\n")

def ReadInput(filename):
    with open(filename,"r") as inputFile:
        for ip in inputFile:
            ips.append(ip.strip())
        

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
    parser.add_argument("-sp", "--specific", action = "store_true", help = "ignore stages and only run specified stage")




#Start of program
parser = argparse.ArgumentParser()
SetParser()
args = parser.parse_args()

                          
ips = []
ipLog = []

#Argument variables
inputfilepath = os.path.abspath(args.input)
saveFolder = args.output
verbose = args.verbose
stages = args.stages
specific = args.specific

#Output filenames
pingName = "results-nmap-ping.txt"
basicName = "results-nmap-basic.txt"
topportsName = "results-nmap-top-ports.txt"
fullscanName = "results-nmap-full.txt"

#try:
ipfile = open(str(inputfilepath), "r")


for ip in ipfile:
    ip = str(ip).strip()
    ips.append(ip)        
    
ipfile.close()

#Create output folder
CreateFolder(saveFolder)

#Run a scan using a specific nmap call
if(specific):
    print("Running specific scan: ", stages)
    if(stages == "ping"):
        #Run the nmap ping only scan to check for live assets
        ipLog = NmapPing(inputfilepath, verbose)
        #Write successful ping results to file
        WriteFiles(pingName, False)

    elif(stages == "basic"):
        #Nmap ports 80,443
        ipLog = Scan(1,basicName, inputfilepath, verbose)
        WriteFiles(basicName, False)

    elif(stages == "topports"):
        #Nmap top 1000 ports
        ipLog = Scan(2,topportsName, inputfilepath, verbose)
        WriteFiles(topportsName, False)

    elif(stages == "full"):
        #Nmap all ports
        ipLog = Scan(3,fullscanName, inputfilepath, verbose)
        WriteFiles(fullscanName, False)
    else:
        pass


#Run a scan in stages       
else:
    #Run the nmap ping only scan to check for live assets
    ipLog = NmapPing(inputfilepath, verbose)


    #Write successful ping results to file
    WriteFiles("results-ping.txt", False)

    ips.clear()        
    ipLog.clear()

    if(stages != "ping"):
        outputfile = "results-dead.txt"
        carryfilepath = os.path.abspath(outputfile)
        ReadInput(carryfilepath)
        #Nmap ports 80,443
        ipLog = Scan(1,"results-nmap1.txt", carryfilepath, verbose)        
        WriteFiles("results-nmap1.txt", False)
        ips.clear()        
        ipLog.clear()
        
        if(stages != "basic"):
            ReadInput(carryfilepath)
            #Nmap top 1000 ports
            ipLog = Scan(2,"results-nmap-.txt", carryfilepath, verbose)
            WriteFiles("results-nmap-top-ports.txt", False)
            ips.clear()        
            ipLog.clear()

            if(stages != "topports"):
                ReadInput(carryfilepath)
                #Nmap all ports
                ipLog = Scan(3,"results-nmap-full.txt", carryfilepath, verbose)
                WriteFiles("results-nmap-full.txt", False)
                ips.clear()        
                ipLog.clear()

print('''
Scan successful, view results in the files created

Goodbye Commander!''')

#except:
 #   print("Could not read file provided")  

