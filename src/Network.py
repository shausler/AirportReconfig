#from igraph.drawing import plot
import collections
import csv
from math import sqrt

import community
import numpy

from NetX import toNetXGraph, partition
from csvLoader import concatNodeAndLookup
import csvLoader
import igraph as ig
import networkx as nx
import numpy as np
import pandas as pd

try:
    import matplotlib.pyplot as plt
except:
    raise

#csvLoader to parse data into a npy
#connection = csvLoader.toConnectionOutfile(num=10000, infileConnections="C:\\Users\\Shane\\Documents\\Airportfiles\\18212900_T_DB1B_COUPON.csv", outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights") #Only needed when using different data from previous invocation"""
connection = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy") #for desktop
#lookup = csvLoader.lookupToOutfile(infileLookup="C:\\Users\\Shane\\Documents\\Airportfiles\\Airport Master Coordinates (2).csv", outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\LookupPickle") #Only needed when using different data from previous invocation"""
lookup = pd.read_pickle("C:\\Users\\Shane\\Documents\\Airportfiles\\LookupPickle")

###LAPTOP load numpy connection graph from *.npy
#connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy") #for laptop
#connections = np.fromfile(file = file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy", )
#csvLoader.lookupEdit(lookup, outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\LookupAdjusted")#may not be needed since pandas

connections = csvLoader.thresholdConnectionsByPassenger(connection, threshNum=10)

nodes = csvLoader.toNodeList(connection,lookup)#convert numpy array connections to node list nodes
#print nodes
"""print "connection"
print connection[0]
print "lookup"
#print type(lookup[4:5]['AIRPORT_SEQ_ID'])
print lookup['AIRPORT_SEQ_ID']"""
#make netX graph with connections(links) and nodes

nAndL = concatNodeAndLookup(nodes, lookup)
gx = toNetXGraph(connection, nodes)
"""nx.draw(gx)
plt.show()"""

#partition(gx)


print "Done"