#from igraph.drawing import plot
import collections
import csv
from math import sqrt
import community
import numpy
import NetX
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

###csvLoader to parse data into a npy
firstTime =         False
doBoth =            False
doThreshByFlight =  True
doThreshByPass =    False
doMarble =          True
doPartition =       False
doAvgPath =         False
doClust =           True

#settings for if you want to reuse big data w/o reprocessing it
freshStart = False
if freshStart:
    firstTime =         True
    doBoth =            False
    doThreshByFlight =  False
    doThreshByPass =    False
    doMarble =          False
    doPartition =       False
    doAvgPath =         False
    doClust =           False

sampleNum = 10000
threshNum = int(sampleNum*(.0005))
threshNum = 0

if firstTime: #if first time, save to disk
    #read in, save raw data for links
    connection = csvLoader.makeConnection(infileConnections="C:\\Users\\Shane\\Documents\\Airportfiles\\18212900_T_DB1B_COUPON.csv",num=sampleNum) 
    np.save("C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection", connection)
    
    #read in, save full lookup table
    lookup = csvLoader.makeLookup(infileLookup="C:\\Users\\Shane\\Documents\\Airportfiles\\Airport Master Coordinates (2).csv") #Only needed when using different data from previous invocation"""
    lookup.to_pickle("C:\\Users\\Shane\\Documents\\Airportfiles\\LookupPickle")
    
        ###LAPTOP load numpy connection graph from *.npy
        #connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection.npy") #for laptop
        #connections = np.fromfile(file = file = "C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection.npy", )
        #csvLoader.lookupEdit(lookup, outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\LookupAdjusted")#may not be needed since pandas
    #threshold if desired
    if doThreshByFlight:
        connection = csvLoader.thresholdConnectionsByFlight(connection, threshNum)
    elif doThreshByPass:
        connection = csvLoader.thresholdConnectionsByPassenger(connection, threshNum)
    
    #pull the nodes from the 
    nodes = csvLoader.toNodeList(connection,lookup)
    
        #make netX graph with connections(links) and nodes
    nodesL = concatNodeAndLookup(nodes, lookup)
    nodesL.to_pickle("C:\\Users\\Shane\\Documents\\Airportfiles\\nodesLPickle")
    print "Saved nodes + lookup"
    del lookup
    del nodes
    print "Deleted lookup \nDeleted nodes"
    print "Correcting connection nodes to match nodes+lookup"
    connection = csvLoader.matchEdgesToNodes(nodesL, connection)
    np.save("C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnectionMatched", connection)    #save numpy array connection to outfile
    print "Saved corrected connection"

    #np.save("C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection1", connection1)    #save numpy array connection to outfile
    gx = NetX.toNetXGraph(connection, nodesL)
    nx.write_gpickle(G=gx, path="C:\\Users\\Shane\\Documents\\Airportfiles\\gxGraph")
    
if not firstTime or doBoth:#if not the first time, load from disk
    connection = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection.npy") #for desktop
    print "Loaded fullConnection from last time"
        ###LAPTOP load numpy connection graph from *.npy
        #connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection.npy") #for laptop
        #connections = np.fromfile(file = file = "C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnection.npy", )
        #csvLoader.lookupEdit(lookup, outfile = "C:\\Users\\Shane\\Documents\\Airportfiles\\LookupAdjusted")#may not be needed since pandas
    if doThreshByFlight:
        connection = csvLoader.thresholdConnectionsByFlight(connection, threshNum)
    elif doThreshByPass:
        connection = csvLoader.thresholdConnectionsByPassenger(connection, threshNum)
    else:
        connection = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\fullConnectionMatched.npy") #for desktop
        print "Loaded last threshed Connection"
    
    nodesL = pd.read_pickle("C:\\Users\\Shane\\Documents\\Airportfiles\\nodesLPickle")
    print "Read nodesL from last time"
    
    gx = nx.read_gpickle("C:\\Users\\Shane\\Documents\\Airportfiles\\gxGraph")
    print "Read gx (nx) from last time"
    #nx.draw(gx)
    #plt.show()
    
    
#Always check for plotting choices    
    
    
if doMarble:
    NetX.blueMarble(gx, nodesL, connection)
if doPartition:
    NetX.partition(gx,nodesL)
    
if doAvgPath:
    avgPL = nx.average_shortest_path_length(G=gx, weight=None)
    print "Average shortest path length:"
    print avgPL
if doClust:
    clust = nx.clustering(G=gx, nodes=None, weight=None)
    print "Clustering:"
    print clust
    #clustArr = np.fromiter(clust.iteritems(), dtype=[('id', '<f8'), ('data', '<f8')], count=len(clust))
    """clustArr = np.array([(k,)+v for k,v in clust.iteritems()], dtype=[('number', '|O4'), ('occurences', '<f8')])
    print clustArr
    histo = np.histogram(a=clustArr)"""
    print "range"
    print range(len(clust))
    plt.bar(range(len(clust)), clust.values(), align='center', width=30)
    #plt.xticks(range(len(clust)), clust.keys())
    plt.show()
    plt.clf()

print "Done"