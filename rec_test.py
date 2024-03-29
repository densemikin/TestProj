#
#		WhiteDNS - A mini DNS server by Dave-ee Jones
#
#		Serves IPs based on domains that are whitelisted. Any queried domains that are not listed are
#		answered with a set IP. Useful for pentesting or for usage in an internal environment, ignoring
#		any external domains/IPs on the internet or other networks.
#
#		ROUTES tutorial:
#			Adding a ROUTE:
#				To add a ROUTE, all you need to do is add an entry to the ROUTES table.
#				E.g. I want 'test' to refer to the IP '10.0.0.1' so I do this:
#				
#				("test.","10.0.0.1")
#				
#				Notice how there is a '.' after 'test'. That is very important and it needs to be added
#				for every entry.
#
#			NOTE:	
#				If you did an nslookup of 'example' and you were under the domain 'test.local' it would 
#				show in the DNS server as 'example.test.local.' because that's the domain you are using. 
#				I have adjusted the server for this so that it only checks the start of a string, ignoring
#				any local domains. However, this can also mean that you can return a different IP for the 
#				same query under different domains.
#				E.g.
#				
#				test.local. 		-> 	127.0.0.1
#				test.company.local. -> 	10.0.0.1
#

import socket, sys, time

### CONFIGURATION ###

ROUTES = [
    ("home.", "0.0.0.0")
]
IP = ""  # Server IP - the IP to listen on (empty string means all)
PORT = 53  # Server Port - the port to listen on
IP_BLACK = "8.8.8.8"  # Blacklist IP - returned if no domain name match in ROUTES
from dns import resolver
DNS_SERVER_MAIN = "8.8.8.8"
ns = resolver.Resolver()
ns.nameservers = [DNS_SERVER_MAIN]

### END CONFIGURATION ###

class dns_query:
    def __init__(self, _data):
        self.data = _data
        self.domain = ""
        self.ip = ""
        kind = (ord(_data[2]) >> 3) & 15
        if kind == 0:
            ini = 12
            lon = ord(_data[ini])
            while lon != 0:
                self.domain += _data[ini + 1:ini + lon + 1] + "."
                ini += lon + 1
                lon = ord(_data[ini])

    def response(self):
        ### WHITELISTING/BLACKLISTING-WITHOUT-A-LIST ###
        packet = ""
        if not self.domain == "":
            for d, a in ROUTES:
                if self.domain.startswith(d):
                    self.ip = a

            if self.ip == "":
                self.ip = ns.query("google.com", "A")


            ### DO NOT CHANGE ANY OF THIS UNLESS YOU KNOW HOW DNS PACKETS WORK ###
            packet += self.data[:2] + "\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + "\x00\x00\x00\x00"
            packet += self.data[12:]
            packet += "\xc0\x0c"
            packet += "\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04"
            packet += str.join("",
                               map(lambda x: chr(int(x)), self.ip.split(".")))

        return packet


### SERVER LAUNCH ###
if __name__ == "__main__":
    sys.stdout.write("[INFO] Starting WhiteDNS server..")
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind((IP, PORT))
    sys.stdout.write("Done.\n")
    print("[INFO] Listening on port %s" % PORT)
    try:
        while 1:
            _data, _addr = udp_server.recvfrom(1024)
            _query = dns_query(_data)
            udp_server.sendto(_query.response(), _addr)
            print("[REQUEST] %s -> %s" % (_query.domain, _query.ip))

    except KeyboardInterrupt:
        sys.stdout.write("[INFO] Shutting down WhiteDNS server..")
        udp_server.close()
        sys.stdout.write("Done.\n")