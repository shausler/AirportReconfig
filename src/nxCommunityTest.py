'''
Created on Sep 30, 2014

@author: Shane
'''
import community
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np

'''
Created on Sep 30, 2014

@author: Shane
'''
import community
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np

#connection = np.zeros((0,6)) #up to 600 cells
#node = np.zeros(500)
infile = ""
infile = "files\\10000.csv"
outfile = ""
outfile = "files\\npArrayFlights"

"""#Column meanings
    0"YEAR",
    1"ORIGIN_AIRPORT_ID",
    2"DEST_AIRPORT_ID",
    3"PASSENGERS",
    4"DISTANCE",
    5"NUM_OF_FLIGHTS",
"""

#read in csv
connection = np.zeros((0,6)) #up to 600 cells
#node = np.zeros(500)
numswapped = 0
 
csvfile = open("files\\10000.csv","rb")    #open your file
dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
csvfile.seek(0)
reader = csv.reader(csvfile, dialect) #read the file, under the dialect
for row in reader: #for each row
    #print str(row) + "\n"
    if(row[1]>row[2]): #if not least to most
        swapper = row[1]
        row[1] = row[2] #make first number least 
        row[2] = swapper # and second number most
        numswapped+=1
        #print "Swapped " + str(numswapped) + "\n"# + str(rownum)
        
        srcloc = np.where(connection[:,1]==int(row[1]))[0]     #where did we find the first node?
        destloc = np.where(connection[:,2]==int(row[2]))[0]     #where did we find the second node?
        
    if(np.any(srcloc==destloc)): # Both in there
        #print "Both in there at " + str(srcloc) + " & " + str(destloc)
        connection[np.where(srcloc==destloc)[0], 5]+=1      #add to the number of flights recorded
        connection[np.where(srcloc==destloc)[0], 3] += float(row[3])                      #add passengers up
        
    elif(np.any(srcloc==destloc) and row[1] != row[2]): # Only the first occurred, so add
        #print "Only the first occurred at " + str(srcloc) + " & " + str(destloc)
        n = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]
        myRow = np.array([n])
        connection = np.vstack((connection,myRow))
        
    else: #Neither in there, so add
        #print "Neither in there"
        n = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]
        #print n
        myRow = np.array([n])
        connection = np.vstack((connection,myRow))
        
print len(connection)
np.save("files\\npArrayFlights", connection)
print "Read/write done"
csvfile.close()    #open your file

print "Done"












from igraph.drawing import plot
try:
    import matplotlib.pyplot as plt
except:
    raise
    
import networkx as nx
import igraph as ig
from math import sqrt
import collections
import numpy
import csv
import community
import csvLoader

"""import sys
print sys.version"""

#processAndWrite(infile = "files\\10000.csv", outfile = "files\\npArrayFlights1.txt")

def toNetXGraph(connection, nodes):
    gx = nx.Graph()
    gx.add_nodes_from(connection[:,])
    

#initialize variables
gx=nx.Graph()
n0=0
n=24
nodeSize=300#nx
fontSize=12#nx
airportCodes = [1,2,3,4,5,6,7]###
numlist = numpy.zeros((500,10))
numlist[0][0]=7
item = 0
category = 0

#create graph in netx
"""gx.add_nodes_from(airportCodes) 
gx.add_edges_from([(1,2), (1,3), (3,2), (3,4), (4,5), (4,6), (6,5), (5,7), (6,7)])"""
gx=nx.watts_strogatz_graph(100, 5, .5)

#infile = file("C:\Users\Shane\workspace\MyAirportNet\\files\First 500.csv") #location
"""counts = collections.Counter()#for example
for line in infile:
   item1 = line.split('whatever delimeter')[0]
   counts[item1] += 1"""
"""#Column meanings
        0"YEAR",
        1"ORIGIN_AIRPORT_ID",
        2"DEST_AIRPORT_ID",
        3"PASSENGERS",
        4"DISTANCE",
        5"NUM_OF_FLIGHTS",
"""

gi1 = ig.Graph(0)
gi1.add_edges([(1,2),(2,3)])
#ig.plot(gi1, layout="kk")


#translate to igraph
nx.write_graphml(gx, "C:/AirportGraph/airGraph")
gi = ig.Graph.Read_GraphML("C:/AirportGraph/airGraph")
#layout = [(0,0), (0,1), (1,1), (1,0)]
#ig.plot(gi, layout=layout)

#gi.add_vertices(4)
#gi.add_edges([(6,8),(7,8),(7,9),(7,10)])
#gi.vs["name"] = ["A", "B", "C", "D", "E", "F", "G"]

"""gi = ig.Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
dist = [9]
layout = gi.layout("circle") #unused"""

"""#create igraph parameter attributes
gi.vs["name"] = ["A", "B", "C", "D", "E", "F", "G"]
gi.vs["lat"] =  [0,0,0,0,0,0,0]
gi.vs["long"] =  [0,1,2,3,4,]"""

#detect communities
#community = gi.community_fastgreedy()
#community = gi.community_multilevel()c
community = gi.community_edge_betweenness() 
layout = gi.layout_sphere()
#ig.plot(gi, layout = layout)
#---sub=gi.subgraph(range(10,50))
#ig.plot(sub, layout ="kk")
"""longe = gi.vs[1]["long"]+gi.vs[2]["long"]
lat = gi.vs[1]["lat"]+gi.vs[2]["lat"]
dist = sqrt(lat^2+longe^2)"""

#move communities back over
#nx.write_gml(community, "C:/AirportGraph/airGraph.gml")######################
gi.write_graphml(f="C:/AirportGraph/airGraph")
gx = nx.read_graphml("C:/AirportGraph/airGraph")

"""plot in netx"""
#nx.draw_shell(gx,node_size=20,font_size=100)
#plt.show()
################################################################################
#first compute the best partition


print "Done"

#selection in igraph
"""print g.vs.select(long_lt=4)["name"] 
print g.vs.select(_degree = g.maxdegree())["name"]
_lt = less than
_eq = equals"""

"""g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
print g.es[0]
g.es[0]["is_formal"] = True
print g.es[0]
g.es[0]["name"] = "Sharon"
print g.es[0]"""

"""g1 = ig.Graph.Tree(127, 2)
g2 = ig.Graph.Tree(127, 2)
print g2.get_edgelist() == g1.get_edgelist()
ig.summary(g1)"""

"""tree = ig.Graph.Tree(127, 2)
g=nx.Graph()##
n0=0
n=24
nodeSize=500
fontSize=12
airportCodes = [1,2,3,4,5,6,7]
g.add_nodes_from(airportCodes)
g.add_edges_from([(1,2), (1,3), (3,2), (3,4), (4,5), (4,6), (6,5), (5,7), (6,7)])
print tree.get_edgelist()
layout=G.layout("kk")
ig.plot(G,layout = layout)
#nx.draw_spring(g,node_size=nodeSize,font_size=fontSize)
#plt.show()"""