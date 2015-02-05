#from igraph.drawing import plot
try:
    import matplotlib.pyplot as plt
except:
    raise

import numpy as np
import networkx as nx
import igraph as ig
from math import sqrt
import collections
import numpy
import csv
import community
import csvLoader

def toNetXGraph(connection, nodes):
    gx = nx.Graph()
    passg = makeEdgeDictFromCol(connection, 4)
    flight = makeEdgeDictFromCol(connection, 6)

    gx.add_nodes_from(nodes)
    print gx.nodes()
    
    gx.add_edges_from(ebunch = connection[:,2:4])       #how to do attributes
    #gx.add_weighted_edges_from(ebunch = connection[:,2:4], weight = "flights", attr = connection[:,6])       #how to do attributes    
    
    #bb=nx.edge_betweenness_centrality(gx, normalized=False)
    #print bb
    #nx.set_edge_attributes(gx, name = 'betweenness', values = bb)
    nx.set_edge_attributes(gx, name = 'passengerCount', values = passg)
    nx.set_edge_attributes(gx, name = 'flights', values = flight)
    #nx.set_node_attributes(gx, name = 'lat', values = )
    
    
    nx.draw_spring(gx,node_size=20,font_size=100)
    plt.show()
    print nx.degree_centrality(gx)
    clique = nx.make_max_clique_graph(gx)
    #plot(obj = clique)
    #nx.set_edge_attributes(gx, name='passengers', values = connection[:,3])
    #nx.set_node_attributes(gx, name='lat', values = )
    
    #print gx.edges(data=True)
    print "NetX loaded"
    return gx
    
def makeEdgeDictFromCol(connection, col):
    #print connection[:,3]
    #print connection[:,1:3]
    myDict = {}
    for x in xrange(0,len(connection)):
        #print x
        #print "(" + str(connection[x,2]) + ", " + str(connection[x,3]) + ")"
        myDict[(connection[x,2], connection[x,3])] = connection[x,col]
    return myDict

#for lat and long
"""def makeNodeDictFromCol(node,col): 
    myDict = {}
    for x in xrange(0,len(node)):
        myDict[(node[x])] = #what needs to go here?
    return myDict
"""

#csvLoader.toOutfile(infile="files\\10000.csv", outfile = "files\\npArrayFlights")
#connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy") #for laptop
connections = np.load(file = "C:\\Users\\Shane\\Documents\\Airportfiles\\npArrayFlights.npy") #for desktop
print connections[:,:]

"""print "Started eliminating:"
x = 0
leng = len(connections)
while x < leng:
    print str(x) + " " + str(connections[x,6])###############################################
    if connections[x,6]<10:
        connections = np.delete(connections, obj = x)
        print "Deleted"
        leng = len(connections)
        x-=1
    x+=1    
print "Finished eliminating. Edges: " + str(len(connections))
"""

#print connections
nodes = csvLoader.toNodeList(connections)
#print nodes
#print nodes
gx = toNetXGraph(connections, nodes)
#nx.draw(gx)
#plt.show()
print "Done"