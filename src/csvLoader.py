from __builtin__ import str
from _ast import Str
import csv
from fileinput import close

import community
from numpy import dtype

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

def makeConnection(infileConnections, num): #read the number of rows from numpy Connections to outfile location
    """dataType = np.dtype([('ID', int),('YEAR', int),('ORIGIN_AIRPORT_SEQ_ID', int),('DEST_AIRPORT_SEQ_ID', int),('PASSENGERS', int),('DISTANCE', int),('NUM_OF_FLIGHTS', int),('QUARTER', int)])
    connection = np.zeros((num,), dtype=dataType) # unique values"""
    connection = np.zeros((num,8),dtype='i64') # unique values
    idn=0
    
    """###Column meanings
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
        2"ORIGIN_AIRPORT_SEQ_ID", (int)
        3"DEST_AIRPORT_SEQ_ID", (int)
        4"PASSENGERS",
        5"DISTANCE",
        6"NUM_OF_FLIGHTS",
        7"QUARTER"
    """
    
    """###infileConnections
        0"YR"
        1"ORIGIN"
        2"DEST"
        3"PASSENGERS"
        4"DIST"
        5"NUM"
    """    """infileConnections
        0"YEAR"
        1"ORIGIN_AIRPORT_SEQ_ID"
        2"QUARTER"
        3"DEST_AIRPORT_SEQ_ID"
        4"PASSENGERS"
        5"DISTANCE"
    """
    print "Reading connections"
    #read in connections csv
    csvfile = open(infileConnections)    #open connections
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file, under the dialect
    csvfile.readline()#get rid of the headings
    
    rowcount=0
    
    for row in reader: 
        if num>0:       #positive number = read that number of rows
            if rowcount > num-1: 
                print "Read ended at row "+str(rowcount)+" " + str(row)#print the first row not read
                break
        
        if(row[1]>row[3]): #if not least to most
            swapper = row[1]
            row[1] = row[3] #make first number least 
            row[3] = swapper # and second number most
        srcloc = np.where(connection[:,2]==int(row[1]))[0]     #where did we find the first node?
        destloc = np.where(connection[:,3]==int(row[3]))[0]     #where did we find the second node?
        
        if(len(np.intersect1d(srcloc,destloc)) > 0): # If both in there
            #---print "Both in there at " + str(srcloc) + " & " + str(destloc)
            #---print "Intersect: " + str(np.intersect1d(srcloc,destloc))
            connection[np.intersect1d(srcloc,destloc), 6] += 1                #add to the number of flights recorded
            connection[np.intersect1d(srcloc,destloc), 4] += float(row[4])    #add passengers up
            
        else: #Not in there, so add
            #---print "Neither in there " + str(myRow[0,1:3])
            """myRow = np.array([[idn, int(row[0]), str(row[1]), str(row[3]), float(row[4]), float(row[5]), float(1), float(row[2])]])
            connection = np.vstack((connection,myRow))"""
            connection[idn]=[idn, int(row[0]), str(row[1]), str(row[3]), float(row[4]), float(row[5]), float(1), float(row[2])]
            idn+=1
        rowcount+=1
        #print connection[:, 1:4] #print column 1-3(2-4?) for all rows 
        #print ""
    connection = connection[0:idn,:]
    #print len(connection)
    #print str(connection)
    csvfile.close()         #close your reader
    print "Read/write done. Edges: " + str(len(connection))
    return connection

def makeLookup(infileLookup):
    #read from lookup
    #http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=288&DB_Short_Name=Aviation%20Support%20Tables
    csvfile = open(infileLookup)    #open lookup
    reader = csv.reader(open(infileLookup,"rb"), delimiter = ',') #read the file, under the dialect
    
    """#Column meanings        (str)
        0"AIRPORT_SEQ_ID"      (int)
        1"AIRPORT_ID",         (int)
        2"AIRPORT",
        3"DISPLAY_AIRPORT_NAME",
        4"DISPLAY_AIRPORT_CITY_NAME_FULL",
        5"AIRPORT_COUNTRY_NAME",
        6"AIRPORT_COUNTRY_CODE_ISO",
        7"AIRPORT_STATE_CODE",
        8"DISPLAY_CITY_MARKET_NAME_FULL",
        9"CITY_MARKET_WAC",
        10"LATITUDE",           (float) 
        11"LONGITUDE",          (float)
        12"AIRPORT_START_DATE",
        13"AIRPORT_THRU_DATE",
        14"AIRPORT_IS_CLOSED"
    """
    """infileConnections
        0"YR"
        1"ORIGIN"
        2"DEST"
        3"PASSENGERS"
        4"DIST"
        5"NUM"
    """
    print "Reading Lookup"
    lookup = pd.read_csv(infileLookup)
    print "Lookup Shape " + str(lookup.shape)
    """print 11
    print lookup[0]
        print "\nExample of lookup 0: " + str(lookup[0])
    print "Read/write done. Lookup Edges: " + str(len(lookup))
    #print "Lookup = " + str(lookup)
    np.save(outfile, lookup)    #save numpy array connection to outfile"""
    #pd.save(df, outfile)
    csvfile.close()         #close your reader
    return lookup
    
#remove connections below certain number of passengers (USE BETWEEN TOARRAY/TOOUTFILE & TONODELIST)

def thresholdConnectionsByFlight(connection, threshNum):
    
    print "Flight threshold start. # of Connections = " + str(len(connection)) +" at threshold = " + str(threshNum)
    x=0                     #from 0 to
    termin=len(connection)  #the last item in connection
    while x < termin:
        #print "On = " + str(x) + ", len = " + str(len(connection))
        if(connection[x,6] <= threshNum):   #find paths with < the threshold of flights (col 6) 
            connection = np.delete(connection, x, 0)    #and remove them from connection
            termin-=1   #adjust for the deleted variable
            x=x-1
        x=x+1   #head on to the next row
    print "Threshold complete. # of Connections = " + str(len(connection))
    return connection

def thresholdConnectionsByPassenger(connection, threshNum):
    
    print "Passenger threshold start. # of Connections = " + str(len(connection)) +" at threshold = " + str(threshNum)
    x=0                     #from 0 to
    termin=len(connection)  #the last item in connection
    while x < termin:
        #print "On = " + str(x) + ", len = " + str(len(connection))
        if(connection[x,4] <= threshNum):   #find paths with < the threshold of passengers 
            connection = np.delete(connection, x, 0)    #and remove them from connection
            termin-=1   #adjust for the deleted variable
            x=x-1
        x=x+1   #head on to the next row
    print "Threshold complete. # of Connections = " + str(len(connection))
    return connection

#create a list of nodes from a numpy array

def toNodeList(connection,lookup):
    """nodes = pd.DataFrame(index = lookup.dtypes)
    for x in xrange(0,len(connection)):
        
    print nodes"""
    
    """
    for all of connection, 
        if connection[1] not in node? (! any cells where node == connection[1])
            add it
        if connection[2] not in node?
            add it
    """
    #connection = #########.
    nodes = np.array(0)
    for x in xrange(0,len(connection)):
        #print x
        if(len(np.intersect1d(nodes, connection[x,2])) == 0):#no intersection means no match
            #print "Added first"
            nodes = np.vstack((nodes,connection[x,2]))
            #print connection[x,1]
        if(len(np.intersect1d(nodes, connection[x,3])) == 0):#no intersection means no match
            #print "Added second"
            nodes = np.vstack((nodes,connection[x,3]))
            #print connection[x,2]
    #print node
    nodes=np.delete(nodes,0)
    nodes = np.sort(nodes)
    #print "Sorted: " + str(node)
    print "NodeList len = " + str(len(nodes))
    return nodes

def concatNodeAndLookup(nodes,lookup):
    
    thisList = []
    for x in xrange(0,len(nodes)):
        """list1=[nodes[x]]
        list1.append(0)
        thisList.append(list1)"""
        thisList.extend([nodes[x],0]) #add the info from node
    nodesL = lookup[lookup['AIRPORT_SEQ_ID'].isin(thisList)] #create table using locations from whereIsIn
    #print df2
    #print len(nodes)
    print "Concatenated Nodes with their lookup"
    nodesL=nodesL.reset_index(drop=True)
    return nodesL

def matchEdgesToNodes(nodesL, connection):
    """replace connection node names with their nodesL index
    """
    print "Matching connection ids to node ids"
    countNp = np.zeros(len(connection))
    for n in xrange(0,len(countNp)): #compare each node id
        for c in xrange(0,len(countNp)): #to the 2 connection ids
            if countNp[c]<2: #if the connection node conversion isn't finished
                if connection[c,2] == nodesL.iloc[n]['AIRPORT_SEQ_ID']: #replace the first node if it matches
                    connection[c,2] = nodesL.index.values[n]
                    countNp[c]+=1
                    #print "c1-------------------------"
                elif connection[c,3] == nodesL.iloc[n]['AIRPORT_SEQ_ID']: #or the second node if it matches
                    connection[c,3] = nodesL.index.values[n]
                    countNp[c]+=1
                    #print "c2--------------------------------------"
    #print countNp
    #print connection[0:3,2:4]
    print "Matched"
    return connection