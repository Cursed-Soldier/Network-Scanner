# Network-Scanner
This is a scanner that identifies 'alive' and 'dead' assets from a given IP list using ping and nmap.

It follows this methodology:
1. Run a ping against the IPs and log which ones respond.
2. Run a nmap scan against port 80 and 443 of the remaining IPs and log which ones respond.
3. Run a nmap scan against the top 1000 ports of the remaining IPs and log which ones respond.
4. Run a nmap scan against the full port range (0-65535) of the remaining IPs and log which ones respond.

## USAGE:
To call the script simply run the command:
`python3 pyscan.py [data.txt] [saveFolder]` where `data.txt` is the list of IP addresses to scan and `saveFolder` is the name of the folder to save the results into.

## OUTPUT:
The program outputs data into the `[saveFolder]` where it is split into different .txt files depending on which part of the scan the IP was confirmed in.

The structure of the output can be seen below:
1. Ping
2. Nmap on port 80 and 443
3. Nmap on top 1000 ports
4. Nmap on full port range (0-65535)
5. Remaining 'dead' IPs
