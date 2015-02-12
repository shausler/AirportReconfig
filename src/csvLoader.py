import community
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np
from fileinput import close
from __builtin__ import str
from _ast import Str


def toConnectionOutfile(infileConnections, outfile, num):
    connection = np.zeros((0,8)) # unique values
    idn=0
    #node = np.zeros(500)
    #numswapped = 0
    #rownum = -1 # so it starts at 0 (only for testing)
    #count=1
    
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
        2"ORIGIN_AIRPORT_ID",
        3"DEST_AIRPORT_ID",
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
    """
    
    """infileConnections
        0"YEAR"
        1"ORIGIN_AIRPORT_SEQ_ID"
        2"QUARTER"
        3"DEST_AIRPORT_SEQ_ID"
        4"PASSENGERS"
        5"DISTANCE"
    """


    #read in connections csv
    csvfile = open(infileConnections)    #open connections
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file, under the dialect
    csvfile.readline()#get rid of the headings
    rowcount=0
    for row in reader: #for each row
        if num>0:
            if rowcount > num+1:
                print "Break at Row = " + str(row) + "\nn="+str(rowcount)+"\nnum= "+str(num)
                break
            rowcount+=1
        
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
            myRow = np.array([[idn, float(row[0]), float(row[1]), float(row[3]), float(row[4]), float(row[5]), float(1), float(row[2])]])
            connection = np.vstack((connection,myRow))
            idn+=1
        #print connection[:, 1:4] #print column 1-3(2-4?) for all rows 
        #print ""
        
    #print len(connection)
    #print str(connection)
    csvfile.close()         #close your reader
    print "Read/write done. Edges: " + str(len(connection))
    np.save(outfile, connection)    #save numpy array connection to outfile
    
#same as toOutfile but doesn't record to numpy array (*.npy)
#instead it returns the array connection
def toArray(infileConnections): 
    connection = np.zeros((0,7)) # unique values
    idn=0
    
    """#Column meanings
        0"ID"
        1"YEAR",
        2"ORIGIN_AIRPORT_ID",
        3"DEST_AIRPORT_ID",
        4"PASSENGERS",
        5"DISTANCE",
        6"NUM_OF_FLIGHTS",
    """
    
    """infileConnections
        0"YR"
        1"ORIGIN"
        2"DEST"
        3"PASSENGERS"
        4"DIST"
        5"NUM"
    """

    #read in csv
    csvfile = open(infileConnections)    #open your file
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file as the dialect
    for row in reader: #for each row
        
        if(row[1]>row[2]): #if not least to most
            swapper = row[1]
            row[1] = row[2] #make first number least 
            row[2] = swapper # and second number most
        
        srcloc = np.where(connection[:,2]==int(row[1]))[0]     #where did we find the first node?
        destloc = np.where(connection[:,3]==int(row[2]))[0]     #where did we find the second node?
        
        if(len(np.intersect1d(srcloc,destloc)) > 0): # Both in there
            #print "Both in there at " + str(srcloc) + " & " + str(destloc)
            #print "Intersect: " + str(np.intersect1d(srcloc,destloc))
            connection[np.intersect1d(srcloc,destloc), 6] += 1                                  #add to the number of flights recorded
            connection[np.intersect1d(srcloc,destloc), 4] += float(row[3])                      #add passengers up
            
        else: #Not in there, so add
            #print "Neither in there " + str(myRow[0,1:3])
            myRow = np.array([[idn, float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]])
            connection = np.vstack((connection,myRow))
            idn+=1
        #print connection[:, 1:4]
        #print ""
        
    #print len(connection)
    #print str(connection)
    csvfile.close()
    print "Read done"
    #print connection
    return connection
    
#processAndWrite(infileConnections = "files\\10000.csv", outfile = "files\\npArrayFlights1.txt")
#n = readToArray(infileConnections = "files\\10000.csv")
#print len(
def lookupToOutfile(infileLookup, outfile):
    lookup = np.zeros((0,15))
    #idn=0
    #node = np.zeros(500)
    #numswapped = 0
    #rownum = -1 # so it starts at 0 (only for testing)
    #count=1
    
    """#Column meanings
        0"AIRPORT_SEQ_ID"
        1"AIRPORT_ID",
        2"AIRPORT",
        3"DISPLAY_AIRPORT_NAME",
        4"DISPLAY_AIRPORT_CITY_NAME_FULL",
        5"AIRPORT_COUNTRY_NAME",
        6"AIRPORT_COUNTRY_CODE_ISO",
        7"AIRPORT_STATE_CODE",
        8"DISPLAY_CITY_MARKET_NAME_FULL",
        9"CITY_MARKET_WAC",
        10"LATITUDE",
        11"LONGITUDE",
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

    #read from lookup
    csvfile = open(infileLookup)    #open lookup
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file, under the dialect
    
    csvfile.readline()
    for row in reader: #for each row
        myRow = np.array([[str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]),str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]), str(row[11]), str(row[12]), str(row[13]), str(row[14])]])
        lookup = np.vstack((lookup,myRow))
    print row
    
    csvfile.close()         #close your reader
    print "Read/write done. Edges: " + str(len(lookup))
    np.save(outfile, lookup)    #save numpy array connection to outfile

#remove connections below certain number of passengers (USE BETWEEN TOARRAY/TOOUTFILE & TONODELIST)
def thresholdConnectionsByPassenger(connection, threshNum):
    
    """for all connections
            if connections[passengerNum] < threshNum
                delete connection
                
    srcloc = np.where(connection[:,2]==int(row[1]))[0]     #where did we find the first node?
    destloc = np.where(connection[:,3]==int(row[2]))[0]     #where did we find the second node?
    """
    """print "Threshold started: Length = " + str(len(connection))
    print "Starting Delete " + str(len(connection ))
    print connection[0,4]
    print "First len = " + str(len(connection))
    print connection[:,4]"""
    x=0                     #from 0 to
    termin=len(connection)  #the last item in connection
    while x < termin:
        #print "On = " + str(x) + ", len = " + str(len(connection))
        if(connection[x,4] <= threshNum):   #find paths with < the threshold of passengers 
            connection = np.delete(connection, x, 0)    #and remove them from connection
            termin-=1   #adjust for the deleted variable
            x=x-1
        x=x+1   #head on to the next row
    print "Threshold complete\nNew Length = " + str(len(connection))
    return connection
    

#create a list of nodes from a numpy array
def toNodeList(connection):
    node = np.array(0)
    """
    for all of connection, 
        if connection[1] not in node? (! any cells where node == connection[1])
            add it
        if connection[2] not in node?
            add it
    """
    #print connection[1,1]
    
    for x in xrange(0,len(connection)):
        #print x
        if(len(np.intersect1d(node, connection[x,2])) == 0):#no intersection means no match
            #print "Added first"
            node = np.vstack((node,connection[x,2]))
            #print connection[x,1]
        if(len(np.intersect1d(node, connection[x,3])) == 0):#no intersection means no match
            #print "Added second"
            node = np.vstack((node,connection[x,3]))
            #print connection[x,2]
    #print node
    node=np.delete(node,0)    
    node = np.sort(node)
    #print "Sorted: " + str(node)
    print "Nodes: " + str(len(node))
    return node