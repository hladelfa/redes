import matplotlib.pyplot as plt
import json
import sys
import os
import networkx as nx
import numpy as np

file_prefix = ''
dpi=300

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

# Pie Quantity Start
pieLabels = []
pieSizes = []
for item in plot_data["type_data"]:
	pieLabels.append(item["id"] + " (" + "{0:.2f}".format(item["percentage"]) + "%)")
	pieSizes.append(int(item["quantity"]))

pie = plt.figure(1)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct='',
	colors=plt.cm.Set1(np.linspace(0., 1., len(pieSizes)))
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Cantidad de paquetes en la red por tipo', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True, fontsize=8)

plt.savefig('output/plot/'+file_prefix+'_pie_type.png', dpi=dpi)
#plt.show()
# Pie Quantity End

# Pie Probability Start
pieLabels = []
pieSizes = []
for item in plot_data["type_data"]:
	pieLabels.append(item["id"] + " (P("+item["id"]+")=" + "{0:.2f}".format(item["probability"]) + ")")
	pieSizes.append(float(item["probability"]))

pie = plt.figure(5)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct='',
	colors=plt.cm.Set1(np.linspace(0., 1., len(pieSizes)))
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Probabilidad por tipo de paquete en la red', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True, fontsize=8)

plt.savefig('output/plot/'+file_prefix+'_pie_type_probability.png', dpi=dpi)
#plt.show()
# Pie Probability End

# Pie Information Start
pieLabels = []
pieSizes = []
for item in plot_data["type_data"]:
	pieLabels.append(item["id"] + " (I("+item["id"]+")=" + "{0:.2f}".format(item["information"]) + ")")
	pieSizes.append(float(item["information"]))

pie = plt.figure(6)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct='',
	colors=plt.cm.Set1(np.linspace(0., 1., len(pieSizes)))
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Informacion por tipo de paquete en la red', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True, fontsize=8)

plt.savefig('output/plot/'+file_prefix+'_pie_type_information.png', dpi=dpi)
#plt.show()
# Pie Information End

# ARP Pie Start
pieLabels = []
pieSizes = []
for item in plot_data["ip_data"]:
	pieLabels.append(item["id"] + " (" + "{0:.2f}".format(item["percentage"]) + "%)")
	pieSizes.append(int(item["quantity"]))

pie = plt.figure(1)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct='',
	colors=plt.cm.Set1(np.linspace(0., 1., len(pieSizes)))
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Cantidad de paquetes en la red por IP', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True, fontsize=8)

plt.savefig('output/plot/'+file_prefix+'_pie_arp.png', dpi=dpi)
#plt.show()
# ARP Pie End

# ARP Pie Probability Start
pieLabels = []
pieSizes = []
for item in plot_data["ip_data"]:
	pieLabels.append(item["id"] + " (P("+item["id"]+")=" + "{0:.2f}".format(item["probability"]) + ")")
	pieSizes.append(float(item["probability"]))

pie = plt.figure(7)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct='',
	colors=plt.cm.Set1(np.linspace(0., 1., len(pieSizes)))
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Probabilidad por IP en la red', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True, fontsize=8)

plt.savefig('output/plot/'+file_prefix+'_pie_arp_probability.png', dpi=dpi)
#plt.show()
# ARP Pie Probability End

# ARP Pie Information Start
pieLabels = []
pieSizes = []
for item in plot_data["ip_data"]:
	pieLabels.append(item["id"] + " (I("+item["id"]+")=" + "{0:.2f}".format(item["information"]) + ")")
	pieSizes.append(float(item["information"]))

pie = plt.figure(8)
patches, texts, autotexts = plt.pie(pieSizes,
	labels=None,
	autopct='',
	colors=plt.cm.Set1(np.linspace(0., 1., len(pieSizes)))
	)

for pie_wedge in patches:
    pie_wedge.set_edgecolor('white')

plt.suptitle('Informacion por IP en la red', fontsize=20)
plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True, fontsize=8)

plt.savefig('output/plot/'+file_prefix+'_pie_arp_information.png', dpi=dpi)
#plt.show()
# ARP Pie Information End

# Type Histogram start
data = plot_data["partial_entropys"]
bins = 20
hist_type = plt.figure(2)
plt.hist(data, bins, color='#8888DD')

plt.suptitle('Histograma de entropia de tipos de paquete en la red', fontsize=20)
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
plt.hist(data, bins, color='#8888DD')

plt.suptitle('Histograma de entropia de direcciones IP en la red', fontsize=20)
plt.xlabel('Entropia')
plt.ylabel('Frecuencia')

plt.grid()

plt.savefig('output/plot/'+file_prefix+'_hist_arp.png', dpi=dpi)
#plt.show()
# ARP Histogram End

# Type information bars start
plt.figure(9)

types = []
index = []
informations = []
num = 0
for item in plot_data["type_data"]:
	num+=1
	types.append(item["id"])
	index.append(num)
	informations.append(item["information"])

plt.bar(index, informations, align='center', color='#8888DD')
plt.xticks(index, types)

plt.suptitle('Informacion de tipos de paquete en la red', fontsize=20)
plt.xlabel('Tipo')
plt.ylabel('Informacion')

entropy = plot_data["partial_entropys"][-1]
plt.plot([0,num+1],[entropy, entropy], c="#FF2222", linewidth=2, label="Entropia")

plt.legend(fontsize=10)

plt.grid()

plt.savefig('output/plot/'+file_prefix+'_information_bars_type.png', dpi=dpi)
#plt.show()
# Type information bars End

# ARP information bars start
plt.figure(10)

ips = []
index = []
informations = []
num = 0
for item in plot_data["ip_data"]:
	num+=1
	ips.append(item["id"])
	index.append(num)
	informations.append(item["information"])

plt.bar(index, informations, align='center', color='#8888DD')
plt.xticks(index, ips, rotation='vertical', fontsize=7)

plt.suptitle('Informacion de IPs en la red', fontsize=20)
plt.xlabel('IP')
plt.ylabel('Informacion')

entropy = plot_data["partial_arp_entropys"][-1]
plt.plot([0,num+1],[entropy, entropy], c="#FF2222", linewidth=2, label="Entropia")

plt.legend(fontsize=10)

plt.grid()

plt.gcf().subplots_adjust(bottom=0.2)

plt.savefig('output/plot/'+file_prefix+'_information_bars_arp.png', dpi=dpi)
#plt.show()
# ARP information bars End

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
	nodeSize = (((quantity - qtyMin) * nodeRange) / (qtyRange if qtyRange != 0 else 1)) + nodeMin
	sizes.append(nodeSize)

edges = []
for packet in plot_data["arp_packets"]:
	edges.append((packet["src"], packet["dst"]))

network = plt.figure(4)
G = nx.DiGraph()
G.add_edges_from(edges)

black_edges = [edge for edge in G.edges()]

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), nodelist=nodes, node_size=sizes, linewidths=0.5, node_color='#AAAAFF')
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False, edge_color='#AAAAAA')
nx.draw_networkx_labels(G,pos,labels,font_size=8, font_weight='bold')

plt.suptitle('Topografia de la red segun paquetes ARP enviados', fontsize=20)

plt.axis('off')

plt.savefig('output/plot/'+file_prefix+'_network.png', dpi=dpi)
# Network End