'''
Created on Feb 5, 2015

@author: Shane
'''
import community
from mpl_toolkits.basemap import Basemap as Basemap
import networkx as nx
from matplotlib.pyplot import winter
from matplotlib import pyplot
import numpy as np

try:
    import matplotlib.pyplot as plt
except:
    raise

"""#Column meanings
        0"ID"
        1"YEAR",
        2"ORIGIN_AIRPORT_ID",
        3"DEST_AIRPORT_ID",
        4"PASSENGERS",
        5"DISTANCE",
        6"NUM_OF_FLIGHTS",
    """
"""#Column meanings
        0"ID"
        1"YEAR",
        2"ORIGIN_AIRPORT_ID",
        3"DEST_AIRPORT_ID",
        4"PASSENGERS",
        5"DISTANCE",
        6"NUM_OF_FLIGHTS",
        7"QUARTER"
    """

#convert list of links and nodes to a networkx graph
def toNetXGraph(connection, nodesL):
    print "Start NetX Graph"
    
    # change to map projection
    
    
    gx = nx.Graph() # empty graph
    #gx.add_nodes_from(nodesL['index'], sId = nodesL['AIRPORT_SEQ_ID'], pos = (nodesL['LATITUDE'],nodesL['LONGITUDE'])) #add netx nodes from the input nodes
    
    gx.add_nodes_from(nodesL.index.values, sId = nodesL['AIRPORT_SEQ_ID']) #add netx nodes from the input nodes
    #gx.add_nodes_from(nodesL['AIRPORT_SEQ_ID']) #add netx nodes from the input nodes
    
    """print 22
    for node in gx.nodes():
        print node
    """
    #gx.add_nodes_from(nodes, pos=(nodes)) #add netx nodes from the input nodes
    #,pos=[(nodesL['LATITUDE'],nodesL['LONGITUDE'])]
    
    
    """gx.add_nodes_from(nodesL['AIRPORT_SEQ_ID']) #add netx nodes from the input nodes
    #gx.add_nodes_from(nodes, pos=(nodes)) #add netx nodes from the input nodes
    #,pos=[(nodesL['LATITUDE'],nodesL['LONGITUDE'])]
    n=0
    for node in gx:
        pos[n]=(mx[n],my[n]) #add in positions
        n+=1
    
    nx.draw_networkx(gx,pos,node_size=100,node_color='red',label = False)
    m.drawcountries()
    m.drawstates()
    m.bluemarble() #map background
    plt.show()"""
    
    
    #---------------------
    gx.add_edges_from(ebunch = connection[:,2:4])       #how to do attributes
    #gx.add_weighted_edges_from(ebunch = connection[:,2:4], weight = "flights", attr = connection[:,6])       #how to do attributes    
    
    #bb=nx.edge_betweenness_centrality(gx, normalized=False)
    #print bb
    #nx.set_edge_attributes(gx, name = 'betweenness', values = bb) #set betweenness from dictionary
    passg = makeEdgeDictFromColumn(connection, 4) #Create dictionary for edges from passenger totals
    flight = makeEdgeDictFromColumn(connection, 6) #create dictionary for edges from the number of aircraft
    
    nx.set_edge_attributes(gx, name = 'passengerCount', values = passg) #set passenger count from dictionary passg
    nx.set_edge_attributes(gx, name = 'flights', values = flight) #set number of aircraft from dictionary flight
    #nx.set_node_attributes(gx, name = 'lat', values = ) #set lattitude for nodes from dictionary
    
    
    """nx.draw_spring(gx,node_size=20,font_size=100)
    plt.show()"""
    #print "Centrality = " + str( nx.degree_centrality(gx))
    clique = nx.make_max_clique_graph(gx)
    #plot(obj = clique)
    #nx.set_edge_attributes(gx, name='passengers', values = connection[:,3])
    #nx.set_node_attributes(gx, name='lat', values = )
    
    #print gx.edges(data=True)
    print "NetX loaded"
    return gx

#Dictionary for edges

def makeEdgeDictFromColumn(connection, col):
    myDict = {}
    for x in xrange(0,len(connection)):
        #print x
        #print "(" + str(connection[x,2]) + ", " + str(connection[x,3]) + ")"
        myDict[(connection[x,2], connection[x,3])] = connection[x,col]
    return myDict
"""def makeNodeDictFromColumn(npNodeArray,lookup): 
    print "Nodes contains:"
    print str(npNodeArray[0])
    print "Lookup contains:"
    print lookup[0,0]
    
    for n in xrange(0,len(npNodeArray)-1):
        code = str(npNodeArray[n])
        #print "Searching mate for " + str(npNodeArray[n])
        for l in xrange(0,len(lookup)-1):
            if lookup[l,0] == code:
                print "found " +  str(lookup[l,0])
                #npNodeArray.set_position(lookup[l,10],lookup[l,11])
                #np.set_position(npNodeArray,(lookup[l,10],lookup[l,11]))
                nx.set_node_attributes(G=npNodeArray, name="position", values=(lookup[l,10],lookup[l,11]))
    #Find the row in lookup that corresponds with each row in node and 
    #apply the lat and long to that node's position
    myDict = {}
    for x in xrange(0,len(npNodeArray)):
        npNodeArray.set_positions()
    return myDict
#for lat and long
    def makeNodeDictFromColumn1(npNodeArray,col,lookup): 
    print npNodeArray
    myDict = {}
    for x in xrange(0,len(npNodeArray)):
        myDict[(npNodeArray[x])] = #what needs to go here?
    npNodeArray.set_positions()
    return myDict
#for lat and long
"""

def blueMarble(gx, nodesL, connection):
    print "Start plotting blue marble"
    plt.figure(num=0, dpi=20)
    m = Basemap(
        projection='merc',
        llcrnrlon=-130,
        llcrnrlat=25,
        urcrnrlon=-60,
        urcrnrlat=50,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)
    
    """m = Basemap(
        projection='merc',
        llcrnrlon=-160,
        llcrnrlat=18,
        urcrnrlon=-70,
        urcrnrlat=50,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)"""
    
    #m = Basemap(projection='robin', lat_0=0, lon_0=-100, resolution='l', area_thresh=1000.0)
    
    m.drawcountries()
    m.drawstates()
    m.bluemarble() #map background
    """#for full earth
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='coral',lake_color='aqua')
    m.drawmapboundary()
    m.drawmeridians(np.arange(0, 360, 30))
    m.drawparallels(np.arange(-90, 90, 30))
    """
    lats = nodesL['LATITUDE'].tolist()
    lons = nodesL['LONGITUDE'].tolist()
    
    mx,my=m(lons,lats)
    pos = {}
    
    #make labels for the marble from the airport names
    labelDict = dict(nodesL.DISPLAY_AIRPORT_NAME)
    #make edge dictionaries
    passg = makeEdgeDictFromColumn(connection, 4) #Create dictionary for edges from passenger totals
    flight = makeEdgeDictFromColumn(connection, 6) #create dictionary for edges from the number of aircraft
    #plot edge colors off passengers(4) or flights(6)
    ec = connection[:,6]
    #plot node size off flight number
    ns = connection[:,6]
    ns=nx.degree(gx)
    print ns
    
    for node in gx:
        pos[node]=(mx[node],my[node]) #add in positions
    nx.draw_networkx(gx, pos, node_size=[v*300 for v in ns.values()], 
                     node_color='red', 
                    labels=labelDict, font_size=25, font_color ='gray',
                    edge_color=ec, edge_cmap=plt.get_cmap('jet')) #draw blue marble nodes
    
    plt.show()
    plt.clf()
    print "Blue marble plotted"
    
def partition(gx,nodesL):
    print "Starting community.partition"
    
    nx.transitivity(gx)
    
    #modularity
    partX= community.best_partition(gx)
    modX = community.modularity(partX, gx)
    
    print "Modularity = " + str(modX)
    
    #plot, color nodes using community structure
    """n=1
    for node in gx.nodes():
        print node
        n=n+1
    print n"""
    labelDict = dict(nodesL.AIRPORT)
    values = [partX.get(node) for node in gx.nodes()]
    nx.draw_spring(gx, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, labels=labelDict)
    #nx.draw(gx, pos)
    plt.show()
    print "Completed partition"
    plt.clf()#clear the plot-