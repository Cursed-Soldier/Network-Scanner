# Network-Scanner

This is a scanner that identifies 'alive' and 'dead' assets from a given IP list using ping and nmap.

It has a variety of options allowing you to conduct a different intensity of scans based on your preference.

  

The 'full' scan follows this methodology:

1. Run a ping against the IPs and log which ones respond.

2. Run a nmap scan against port 80 and 443 of the remaining IPs and log which ones respond.

3. Run a nmap scan against the top 1000 ports of the remaining IPs and log which ones respond.

4. Run a nmap scan against the full port range (0-65535) of the remaining IPs and log which ones respond.

  

There are options to only do steps 1, 1-2 or 1-3 if a full scan is not required.

  

## USAGE:

### Running the Script
To use the script, follow the instructions below:

For Linux:
`python3 pyscan.py [-h] -i INPUT [-o OUTPUT] [-v] [-s {ping,basic,topports,full}]` 

For Windows:
`python pyscan.py [-h] -i INPUT [-o OUTPUT] [-v] [-s {ping,basic,topports,full}]`

### Options:

`-h`, `--help` show this help message and exit

`-i INPUT`, `--input INPUT` input file (.txt) with the IPs to be used in the network scan

`-o OUTPUT`, `--output OUTPUT` name of the output folder to be used (default = results)

`-v`, `--verbose` verbose message option
scan intensity selector

`-s {ping,basic,topports,full}`, `--stages {ping,basic,topports,full}` scan intensity selector

## OUTPUT:

The program outputs data into the provided `OUTPUT` folder where it is split into different .txt files depending on which part of the scan the IP was confirmed in.

  

The structure of the output can be seen below:

1. Ping
2. Nmap on port 80 and 443
3. Nmap on top 1000 ports
4. Nmap on full port range (0-65535)
5. Remaining 'dead' IPs

This output is possible for a full scan only. If another stage is chosen or there is nothing to put into a specific output, the files will not be created.
