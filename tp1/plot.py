import matplotlib.pyplot as plt
import json
import numpy
import sys
import os

file_prefix = ''

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

plt.axis('equal')

plt.legend(patches, pieLabels, loc=(-0.05, 0.05), shadow=True)

plt.savefig('output/plot/'+file_prefix+'_pie.png')
#plt.show()
# Pie End

# Type Histogram start
data = plot_data["partial_entropys"]
bins = 20
hist_type = plt.figure(2)
plt.hist(data, bins)

plt.xlabel('Entropia')
plt.ylabel('Frecuencia')

plt.savefig('output/plot/'+file_prefix+'_hist_type.png')
#plt.show()
# Type Histogram End

# ARP Histogram start
data = plot_data["partial_arp_entropys"]
bins = 20

hist_arp = plt.figure(3)
plt.hist(data, bins)

plt.xlabel('Entropia')
plt.ylabel('Frecuencia')

plt.savefig('output/plot/'+file_prefix+'_hist_arp.png')
#plt.show()
# ARP Histogram End
