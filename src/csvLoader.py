import community
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np
from fileinput import close
from __builtin__ import str

def toOutfile(infile, outfile):
    connection = np.zeros((0,7)) # unique values
    idn=0
    #node = np.zeros(500)
    #numswapped = 0
    #rownum = -1 # so it starts at 0 (only for testing)
    #count=1
    
    """#Column meanings
        0"ID"
        1"YEAR",
        2"ORIGIN_AIRPORT_ID",
        3"DEST_AIRPORT_ID",
        4"PASSENGERS",
        5"DISTANCE",
        6"NUM_OF_FLIGHTS",
    """
    
    """Infile
        0"YR"
        1"ORIGIN"
        2"DEST"
        3"PASSENGERS"
        4"DIST"
        5"NUM"
    """

    #read in csv
    csvfile = open(infile)    #open your file
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file, under the dialect
    for row in reader: #for each row
        #print str(count)
        #count += 1
        
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
            #print "Neither in there"
            myRow = np.array([[idn, float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]])
            #print "Neither in there " + str(myRow[0,1:3])
            connection = np.vstack((connection,myRow))
            idn+=1
        #print connection[:, 1:4]
        #print ""
        
    #print len(connection)
    #print str(connection)
    #print str(numTF) + " " + str(numFF)
    csvfile.close()
    print "Read/write done. Edges: " + str(len(connection))
    np.save(outfile, connection)
    
def toArray(infile):
    connection = np.zeros((0,7)) # unique values
    idn=0
    #node = np.zeros(500)
    #numswapped = 0
    #rownum = -1 # so it starts at 0 (only for testing)
    #count=1
    
    """#Column meanings
        0"ID"
        1"YEAR",
        2"ORIGIN_AIRPORT_ID",
        3"DEST_AIRPORT_ID",
        4"PASSENGERS",
        5"DISTANCE",
        6"NUM_OF_FLIGHTS",
    """
    
    """Infile
        0"YR"
        1"ORIGIN"
        2"DEST"
        3"PASSENGERS"
        4"DIST"
        5"NUM"
    """

    #read in csv
    csvfile = open(infile)    #open your file
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file, under the dialect
    for row in reader: #for each row
        #print str(count)
        #count += 1
        
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
            #print "Neither in there"
            myRow = np.array([[idn, float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]])
            #print "Neither in there " + str(myRow[0,1:3])
            connection = np.vstack((connection,myRow))
            idn+=1
        #print connection[:, 1:4]
        #print ""
        
    #print len(connection)
    #print str(connection)
    #print str(numTF) + " " + str(numFF)
    csvfile.close()
    print "Read done"
    #print len(connection)
    #print connection
    return connection
    
#processAndWrite(infile = "files\\10000.csv", outfile = "files\\npArrayFlights1.txt")

#n = readToArray(infile = "files\\10000.csv")
#print len(n)

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
