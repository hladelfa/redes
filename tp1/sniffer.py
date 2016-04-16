#! /usr/bin/env python
from scapy.all import *
import json

total_packets = 0.0
total_ips = 0.0
packet_types = {}
packet_names = {}
ips = {}
file_prefix = ""
in_timeout = 10
in_filter_arp = "" 
file
arp_file = ""
type_file = ""
arp_text= {
    1 : "ARP:who-has",
    2 : "ARP:is-at"
} 
partial_entropys = []
partial_arp_entropys = []

plot_data = {}
plot_data["type_data"] = []
plot_data["ip_data"] = []
plot_data["arp_packets"] = []
plot_data["arp_ip_packet_quantity"] = {}

if len(sys.argv) > 1:
    file_prefix = sys.argv[1] 
else:
    print("Usage: sniffer.py FILE_PREFIX [TIMEOUT] [FILTER]")
    sys.exit(0) 

if len(sys.argv) > 2:
    in_timeout = float(sys.argv[2])  

if len(sys.argv) > 3:
    in_filter_arp = sys.argv[3] 

outputDir = "log/"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

def writeNodeToFile(pkt,file):
    packetInfo =  time.strftime("%d/%m/%y - %H:%M:%S")
    packetInfo += " -- "
    if ARP in pkt:
        packetInfo += pkt[1].hwsrc
        packetInfo += " -- "
        packetInfo += pkt[1].hwdst
        packetInfo += " -- "
        packetInfo += pkt[1].psrc
        packetInfo += " -- "
        packetInfo += pkt[1].pdst
        packetInfo += " : "        
        packetInfo += arp_text[pkt[1].op]
    else:    
        packetInfo += pkt.src
        packetInfo += " -- "
        packetInfo += pkt.dst
        packetInfo += " -- "
        
        if IP in pkt:
                packetInfo += pkt[IP].src
                packetInfo += " -- "
                packetInfo += pkt[IP].dst
        else:
		if IPv6 in pkt:
                	packetInfo += pkt[IPv6].src
                	packetInfo += " -- "
                	packetInfo += pkt[IPv6].dst
		else:
			packetInfo += "no ip"
                	packetInfo += " -- "
                	packetInfo += "no ip"
        packetInfo += " -- "
        packetInfo += pkt[1].name
        

    packetInfo += '\n'
    file.write(packetInfo)

def monitor_callback(pkt):

    #print(pkt.show())
    #writeNodeToFile(pkt,file)

    if in_filter_arp != "arp":
    	entropy_values(pkt) 

    arp_entropy_values(pkt)  
    add_partial_entropy() 

def entropy_values(pkt):
    global total_packets 
    total_packets += 1 
    
    if pkt[1].name == 'LLC' or pkt[1].name == 'UDP' or pkt[1].name == 'ICMP':        
        key = pkt[1].name
    else:
        key = pkt[Ether].type      

    if packet_types.get(key) != None:
        packet_types[key] += 1  
    else:
        packet_types[key] = 1
        packet_names[key] = pkt[1].name

def arp_entropy_values(pkt):
    global total_ips 
    
    if pkt[1].name == 'ARP':	
    	total_ips += 2 
    	psrc = pkt[ARP].psrc
    	pdst = pkt[ARP].pdst
    	if ips.get(psrc) != None:
        	ips[psrc] += 1  
    	else:
        	ips[psrc] = 1

    	if ips.get(pdst) != None:
        	ips[pdst] += 1
    	else:
        	ips[pdst] = 1

        plot_data["arp_packets"].append({'src':psrc, 'dst':pdst})
 
def add_partial_entropy():
    global total_packets
    global packet_types
    entropy = 0.0
    arp_entropy = 0.0

    for type in packet_types:
        prob = packet_types[type]/total_packets
        info = -math.log(prob,2)
        entropy = entropy + (prob * info)

    partial_entropys.append(entropy)

    for ip in ips:
        prob = ips[ip]/total_ips
        info = -math.log(prob,2)
        arp_entropy = arp_entropy + (prob * info)

    partial_arp_entropys.append(arp_entropy)

def calculate_entropy():
    global total_packets
    global packet_types 
    entropy = 0.0
    arp_entropy = 0.0

    for type in packet_types:
        type_file.write(packet_names[type]+"("+str(type)+") Paquetes: "+str(packet_types[type])+"\n")
        prob = packet_types[type]/total_packets
        type_file.write(packet_names[type]+" P("+str(type)+") = "+str(prob)+"\n")
        info = -math.log(prob,2)
        type_file.write(packet_names[type]+" I("+str(type)+") = "+str(info)+"\n")
        entropy = entropy + (prob * info)

        plot_data["type_data"].append({
            'id':packet_names[type],
            'quantity':packet_types[type],
            'probability':prob,
            'information':info,
            'percentage':packet_types[type]*100/total_packets
        })

    type_file.write("H(S) = "+str(entropy)+"\n")

    for ip in ips:
        arp_file.write(ip+" Paquetes: "+str(ips[ip])+"\n")
        prob = ips[ip]/total_ips
        arp_file.write(ip+" P("+ip+") = "+str(prob)+"\n")
        info = -math.log(prob,2)
        arp_file.write(ip+" I("+ip+") = "+str(info)+"\n")
        arp_entropy = arp_entropy + (prob * info)

        plot_data["ip_data"].append({
            'id':ip,
            'quantity':ips[ip],
            'probability':prob,
            'information':info,
        })
        plot_data["arp_ip_packet_quantity"][ip] = ips[ip]

    arp_file.write("H(S) = "+str(arp_entropy)+"\n")	


fecha = time.strftime("%d-%m-%y-%H:%M:%S")
file = open('log/nodes_'+fecha, 'w')
if __name__ == '__main__':
        sniff(prn=monitor_callback, timeout = in_timeout, filter = in_filter_arp)
file.close()

arp_file = open('log/arp_entropy_'+fecha, 'w')
type_file = open('log/type_entropy_'+fecha, 'w')
calculate_entropy()
arp_file.close()
type_file.close()

plot_data["partial_entropys"] = partial_entropys
plot_data["partial_arp_entropys"] = partial_arp_entropys

outputDir = "output/data/"
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
plot_data_file = open("output/data/"+file_prefix+"_plotData.json","w")
json.dump(plot_data,plot_data_file, indent=4)                                    
plot_data_file.close()