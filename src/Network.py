#from igraph.drawing import plot
import collections
import csv
from math import sqrt

import community
import numpy

from NetX import toNetXGraph, partition
import csvLoader
import igraph as ig
import networkx as nx
import numpy as np
try:
    import matplotlib.pyplot as plt
except:
    raise

#csvLoader to parse data into a npy
csvLoader.toConnectionOutfile(infileConnections="C:\\Users\\Shane\\Documents\\Airportfiles\\18212900_T_DB1B_COUPON.csv",
                               outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights",
                               num=100) #Only needed when using different data from previous invocation


"""csvLoader.lookupToOutfile(infileLookup="C:\\Users\\Shane\\Documents\\Airportfiles\\Airport Master Coordinates.csv",
outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlightsLookup") #Only needed when using different data from previous invocation"""

#load numpy connection graph from *.npy
#connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy") #for laptop
connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy") #for desktop
lookup = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlightsLookup.npy") #for desktop
#print "Connections " + str(connections[:,:])
#print lookup[:,:]

connections = csvLoader.thresholdConnectionsByPassenger(connections, 0)

nodes = csvLoader.toNodeList(connections)#convert numpy array connections to node list nodes
#print nodes

#make netX graph with connections(links) and nodes
gx = toNetXGraph(connections, nodes)
"""nx.draw(gx)
plt.show()"""
partition(gx)

print "Done"