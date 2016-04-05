#! /usr/bin/env python
from scapy.all import *

total_packets = 0.0
packet_types = {}
packet_names = {}
in_timeout = 10
in_filter_arp = "" 

if len(sys.argv) > 1:
    in_timeout = float(sys.argv[1])  

if len(sys.argv) > 2:
    in_filter_arp = sys.argv[2] 

def monitor_callback(pkt):
    if in_filter_arp != "":
        arp_entropy_values(pkt)
    else:         
        entropy_values(pkt)    
    print pkt.show()

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
    global total_packets 
    total_packets += 2 
    psrc = pkt[ARP].psrc
    pdst = pkt[ARP].pdst
    if packet_types.get(psrc) != None:
        packet_types[psrc] += 1  
    else:
        packet_types[psrc] = 1
        packet_names[psrc] = pkt[1].name

    if packet_types.get(pdst) != None:
        packet_types[pdst] += 1
    else:
        packet_types[pdst] = 1
        packet_names[pdst] = pkt[1].name     

def calculate_entropy():
    global total_packets
    global packet_types     
    print total_packets
    entropy = 0.0

    for type in packet_types:
        print packet_names[type]+"("+str(type)+") Paquetes: "+str(packet_types[type])+"\n"
        prob = packet_types[type]/total_packets
        print packet_names[type]+" P("+str(type)+") = "+str(prob)+"\n"
        info = -math.log(prob,2)
        print packet_names[type]+" I("+str(type)+") = "+str(info)+"\n"
        entropy = entropy + (prob * info)

    print "H(S) = "+str(entropy)+"\n"	

if __name__ == '__main__':
        sniff(prn=monitor_callback, timeout = in_timeout, filter = in_filter_arp)

calculate_entropy()


