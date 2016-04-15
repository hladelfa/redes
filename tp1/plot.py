import matplotlib.pyplot as plt
import json
from numpy import random
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
	pieLabels.append(item["id"])
	pieSizes.append(int(item["quantity"]))

pie = plt.figure(1)
plt.pie(pieSizes,
	labels=pieLabels,
	autopct='%1.1f%%'
	)

plt.axis('equal')

plt.savefig('output/plot/'+file_prefix+'_pie.png')
#plt.show()
# Pie End

# Type Histogram start
data = plot_data["partial_entropys"]
bins = 20
hist_type = plt.figure(2)
plt.hist(data, bins)

#plt.legend()

plt.savefig('output/plot/'+file_prefix+'_hist_type.png')
#plt.show()
# Type Histogram End

# ARP Histogram start
data = plot_data["partial_arp_entropys"]
bins = 20

hist_arp = plt.figure(3)
plt.hist(data, bins)

#plt.legend()

plt.savefig('output/plot/'+file_prefix+'_hist_arp.png')
#plt.show()
# ARP Histogram End
