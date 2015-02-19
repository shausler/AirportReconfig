'''
Created on Feb 5, 2015

@author: Shane
'''
import community

import networkx as nx


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
def toNetXGraph(connection, nodes):
    gx = nx.Graph() # empty graph
    
    passg = makeEdgeDictFromColumn(connection, 4) #Create dictionary for edges from passenger totals
    flight = makeEdgeDictFromColumn(connection, 6) #create dictionary for edges from the number of aircraft
    """---------------------------------------"""
    gx.add_nodes_from(nodes) #add netx nodes from the input nodes
    #gx.add_nodes_from(nodes, pos=(nodes)) #add netx nodes from the input nodes
   
    gx.add_edges_from(ebunch = connection[:,2:4])       #how to do attributes
    #gx.add_weighted_edges_from(ebunch = connection[:,2:4], weight = "flights", attr = connection[:,6])       #how to do attributes    
    
    #bb=nx.edge_betweenness_centrality(gx, normalized=False)
    #print bb
    #nx.set_edge_attributes(gx, name = 'betweenness', values = bb) #set betweenness from dictionary
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
def partition(gx):
    nx.transitivity(gx)
    
    #modularity
    partX= community.best_partition(gx)
    modX = community.modularity(partX, gx)
    
    print "Modularity = " + str(modX)
    
    #plot, color nodes using community structure
    values = [partX.get(node) for node in gx.nodes()]
    nx.draw_spring(gx, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
    plt.show()   