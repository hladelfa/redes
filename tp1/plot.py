import matplotlib.pyplot as plt
import json
import sys
import os
import networkx as nx
import numpy as np

file_prefix = ''
dpi=500

if len(sys.argv) > 1:
    file_prefix = sys.argv[1]
else:
    print("Usage: plot.py FILE_PREFIX")
    sys.exit(0) 

fileName = 'output/data/'+file_prefix+'_plotData.json'
outputDir = "output/plot/"
if not os.path.exists(outputDir):
	os.makedirs(outputDir)

with open(fileName) as file_data:    
	plot_data = json.load(file_data)

# Pie Start
pieLabels = []
pieSizes = []
for item in plot_data["type_data"]:
	pieLabels.append(item["id"] + " (" + "{0:.2f}".format(item["percentage"]) + "%)")
	pieSizes.append(int(item["quantity"]))

pie = plt.figure(1)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct=''
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Tipos de paquete en la red', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True)

plt.savefig('output/plot/'+file_prefix+'_pie.png', dpi=dpi)
#plt.show()
# Pie End

# Type Histogram start
data = plot_data["partial_entropys"]
bins = 20
hist_type = plt.figure(2)
plt.hist(data, bins)

plt.suptitle('Entropia de tipos de paquete en la red', fontsize=20)
plt.xlabel('Entropia')
plt.ylabel('Frecuencia')

plt.grid()

plt.savefig('output/plot/'+file_prefix+'_hist_type.png', dpi=dpi)
#plt.show()
# Type Histogram End

# ARP Histogram start
data = plot_data["partial_arp_entropys"]
bins = 20

hist_arp = plt.figure(3)
plt.hist(data, bins)

plt.suptitle('Entropia de direcciones IP en la red', fontsize=20)
plt.xlabel('Entropia')
plt.ylabel('Frecuencia')

plt.grid()

plt.savefig('output/plot/'+file_prefix+'_hist_arp.png', dpi=dpi)
#plt.show()
# ARP Histogram End

# Network Start
nodes = []
quantities = []
labels = {}
for node in plot_data["ip_data"]:
	nodes.append(node["id"])
	quantities.append(node["quantity"])
	labels[node["id"]]=node["id"]

sizes = []
for quantity in quantities:
	qtyMin = min(quantities)
	qtyMax = max(quantities)
	qtyRange = (qtyMax - qtyMin)  
	nodeMin = 300
	nodeMax = 4000
	nodeRange = (nodeMax - nodeMin)  
	nodeSize = (((quantity - qtyMin) * nodeRange) / qtyRange) + nodeMin
	sizes.append(nodeSize)

edges = []
for packet in plot_data["arp_packets"]:
	edges.append((packet["src"], packet["dst"]))

network = plt.figure(4)
G = nx.DiGraph()
G.add_edges_from(edges)

black_edges = [edge for edge in G.edges()]

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), nodelist=nodes, node_size=sizes, alpha=0.7, linewidths=0.5, node_color='#AAAAFF')
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False, edge_color='#AAAAAA')
nx.draw_networkx_labels(G,pos,labels,font_size=8, font_weight='bold')

plt.axis('off')

plt.savefig('output/plot/'+file_prefix+'_network.png', dpi=dpi)
# Network End