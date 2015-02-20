from __builtin__ import str
from _ast import Str
import csv
from fileinput import close

import community
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from numpy import dtype




def toConnectionOutfile(infileConnections, outfile, num): #read the number of rows from numpy Connections to outfile location
    """dataType = np.dtype([('ID', int),('YEAR', int),('ORIGIN_AIRPORT_SEQ_ID', int),('DEST_AIRPORT_SEQ_ID', int),('PASSENGERS', int),('DISTANCE', int),('NUM_OF_FLIGHTS', int),('QUARTER', int)])
    connection = np.zeros((num,), dtype=dataType) # unique values"""
    connection = np.zeros((num,8),dtype='i64') # unique values
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
    #read in connections csv
    csvfile = open(infileConnections)    #open connections
    dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect) #read the file, under the dialect
    csvfile.readline()#get rid of the headings
    """allConnections = np.genfromtxt(fname=infileConnections, dtype=None, delimiter=",", names=True) # make sure headings still there
    print 1
    print len(allConnections)"""
    rowcount=0
    
    for row in reader: 
        if num>0:       #positive number = read that number of rows
            if rowcount > num-1: 
                print "Read end at row "+str(rowcount)+" " + str(row) +"\nnum= "+str(num)#print the first row not read
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
    np.save(outfile, connection)    #save numpy array connection to outfile
    return connection
    
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
    #read from lookup
    #http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=288&DB_Short_Name=Aviation%20Support%20Tables
    csvfile = open(infileLookup)    #open lookup
    reader = csv.reader(open(infileLookup,"rb"), delimiter = ',') #read the file, under the dialect
    
    """#trying with loadtxt, dtype
    dt = np.dtype([('AIRPORT_SEQ_ID','i8'),('AIRPORT_ID','i8'), #the ints 
                         ('AIRPORT','a4'),('DISPLAY_AIRPORT_NAME','a64'),
                         ('DISPLAY_AIRPORT_CITY_NAME_FULL','a64'),('AIRPORT_COUNTRY_NAME','a4'),
                         ('AIRPORT_COUNTRY_CODE_ISO','a64'),('AIRPORT_STATE_CODE','a4'),
                         ('DISPLAY_CITY_MARKET_NAME_FULL','f32'),('CITY_MARKET_WAC',str),
                         ('LATITUDE','f32'),('LONGITUDE','f32'), #the floats
                         ('AIRPORT_START_DATE','a32'),('AIRPORT_THRU_DATE','a32'),('AIRPORT_IS_CLOSED','b1')])
    l=list(reader)
    dt = np.dtype('i8, i8, a4, a64, a64, a4, a64, a4, f32, f32, a32, a32, b1')
    dt = np.dtype('i8, i8, a4, a64, a64, a4,a64, a4,a4,a4,a4, f32, f32, a32, a32, b1')
    dt = np.dtype([('AIRPORT_SEQ_ID','i8'),('AIRPORT','a3'),
                  ('DISPLAY_AIRPORT_NAME','a48'),('AIRPORT_WAC','i4'),
                  ('AIRPORT_COUNTRY_NAME','a48'),('AIRPORT_COUNTRY_CODE','a2'),
                  ('AIRPORT_STATE_NAME','a48'),('AIRPORT_STATE_CODE','a2'),('AIRPORT_STATE_FIPS','i8'),
                  ('CITY_MARKET_ID','i8'),('LAT_DEGREES','i8'),('LAT_HEMISPHERE','a1'),
                  ('LAT_MINUTES','i8'),('LAT_SECONDS','i8'),('LATITUDE','i48'),('LON_DEGREES','i8'),
                  ('LON_HEMISPHERE','a1'),('LON_MINUTES','i8'),('LON_SECONDS','i8'),
                  ('LONGITUDE','i48'),('AIRPORT_START_DATE','a16'),('AIRPORT_IS_CLOSED','b1')])
    dt = np.dtype('i8, a3, a48, i4, a48, a2, a48, a2, i8, i8, i8, a1, i8, i8, i48, i8, a1, i8, i8, i48, a16, b1')
    lookup = np.loadtxt(open(infileLookup,'rb'), delimiter="," , skiprows=1 ,dtype=dt)#,usecols=(0,1,2,3,4,5,6,11,12)
    #lookup = np.array(l).astype('i8, i8, a4, a48, a12, a12, a32, a4, a4, a12, a12, i4, a16, a16, a16, a16, b1')"""
    #np.fromregex(infileLookup, r'(\d+),"(.+)",(\d+)', 'i8, S20, i8')
    #lookup = np.array(l).astype(str)
    #dt = np.dtype('a32')
    #lookup = np.zeros((12633,16),dtype = ("a8, a8, a4, a48, a48, a32, a4, a4, a32, i4, f16, f16, a16, a16, b1"))
    #lookup = np.fromfile(file = csvfile, dtype = ("a8, a8, a4, a48, a48, a32, a4, a4, a32, i4, f16, f16, a16, a16, b1"),count =-1, sep = ",")
    #lookup = np.zeros((12633,16),dtype = 'a32')
    #print type(lookup[0,0])
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
    """#trying with if-for
    rowNum=0
    csvfile.readline()
    lookup = np.zeros((0,16)) # unique values
    for row in reader:                  #for each row
        if row[1] != "99999":           #as long as it's not the fake last flight
            #print "11 Current row = " + str(row)
            lookup[rowNum]=row
            for x in xrange(0,16):      #load the 14 vars
                print "Row "+str(x)+" = " + str(row[x])
                if x == 0 or x == 1:                    #0,1 are the seq and reg IDs
                    row[x] = int(row[x])
                elif x == 10 or x == 11:             #10,11 are the lat and long
                    row[x] = float(row[x])
                else:
                    row[x] = str(row[x])
            lookup[rowNum]=row
        rowNum=rowNum+1"""
    #trying with vstack, works for string
    """dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
    csvfile.seek(0)
    reader = csv.reader(csvfile,dialect)"""
    
    lookup = pd.read_csv(infileLookup)
    print lookup.shape
    
    #csvfile.readline()
    
    """rowNum=0
    thisList = [[0 for x in range(22) for x in range(12706)]]
    for row in reader:              #for each row
        for x in xrange(0,21):
            thisList[rowNum][x]=row[rowNum][x]
        rowNum+=1
    print thisList
    return thisList"""

    """lookup = np.zeros((0,22)) # unique values
    for row in reader:              #for each row
        myRow = np.array([[(row[0]), (row[1]), (row[2]), (row[3]), (row[4]), (row[5]), (row[6]), (row[7]), (row[8]), (row[9]), (row[10]), (row[11]), (row[12]), (row[13]), (row[14]), (row[15]), (row[16]), (row[17]), (row[18]), (row[19]), (row[20]), (row[21])]])
        lookup = np.vstack((lookup,myRow))#"""
    """#trying with list
    rowNum=0
    mylist=list
    csvfile.readline()
    lookup = np.empty((0,16)) # unique values
    for row in reader:                  #for each row
        print row
        mylist = mylist.append(row)
    lookup = np.array(mylist)#"""
        
    """print 11
    print lookup[0]
        print "\nExample of lookup 0: " + str(lookup[0])
    print "Read/write done. Lookup Edges: " + str(len(lookup))
    #print "Lookup = " + str(lookup)
    np.save(outfile, lookup)    #save numpy array connection to outfile"""
    #pd.save(df, outfile)
    lookup.to_pickle(outfile)
    csvfile.close()         #close your reader
    return lookup
    
#remove connections below certain number of passengers (USE BETWEEN TOARRAY/TOOUTFILE & TONODELIST)
def lookupEdit(lookup, outfile):
    lookup = np.delete(lookup,0,0)
    lookup = np.delete(lookup,-1,0)
    print str(1) + " "+ str(lookup[0]) + " len "+ str(len(lookup))
    for x in xrange(0,len(lookup)-1):
        for n in xrange(0,21):
            if lookup[x,n] == '':
                lookup[x,n]=0
                #print "Changed location: "+ str(x)+" "+str(n)+ " to " + lookup[x,n]
    print str(2) + " "+ str(lookup[0]) + " len "+ str(len(lookup))
    
    dt = np.dtype("i8, a3, a48, i4, a48, a2, a48, a2, i8, i8, i8, a1, i8, i8, i48, i8, a1, i8, i8, i48, a16, b1")
    """dt = np.dtype([('AIRPORT_SEQ_ID','i8'),('AIRPORT','a3'),
                  ('DISPLAY_AIRPORT_NAME','a48'),('AIRPORT_WAC','i4'),
                  ('AIRPORT_COUNTRY_NAME','a48'),('AIRPORT_COUNTRY_CODE','a2'),
                  ('AIRPORT_STATE_NAME','a48'),('AIRPORT_STATE_CODE','a2'),('AIRPORT_STATE_FIPS','i8'),
                  ('CITY_MARKET_ID','i8'),('LAT_DEGREES','i8'),('LAT_HEMISPHERE','a1'),
                  ('LAT_MINUTES','i8'),('LAT_SECONDS','i8'),('LATITUDE','i48'),('LON_DEGREES','i8'),
                  ('LON_HEMISPHERE','a1'),('LON_MINUTES','i8'),('LON_SECONDS','i8'),
                  ('LONGITUDE','i48'),('AIRPORT_START_DATE','a16'),('AIRPORT_IS_CLOSED','b1')])"""
    dt = np.dtype([('AIRPORT_SEQ_ID','i8'),('AIRPORT','a3'),('DISPLAY_AIRPORT_NAME','a48'),('AIRPORT_WAC','i4'),('AIRPORT_COUNTRY_NAME','a48'),('AIRPORT_COUNTRY_CODE','a2'),('AIRPORT_STATE_NAME','a48'),('AIRPORT_STATE_CODE','a2'),('AIRPORT_STATE_FIPS','i8'),('CITY_MARKET_ID','i8'),('LAT_DEGREES','i8'),('LAT_HEMISPHERE','a1'),('LAT_MINUTES','i8'),('LAT_SECONDS','i8'),('LATITUDE','i48'),('LON_DEGREES','i8'),('LON_HEMISPHERE','a1'),('LON_MINUTES','i8'),('LON_SECONDS','i8'),('LONGITUDE','i48'),('AIRPORT_START_DATE','a16'),('AIRPORT_IS_CLOSED','b1')])
    dt = np.dtype(np.str)
    newLookup = np.array(lookup, dtype=dt)
    #print newLookup[-1]
    np.save(outfile, lookup)    #save numpy array connection to outfile
    """for x in xrange(0,len(lookup)-1):
        for n in xrange(0,21):
            if n==0 or n==3 or n==8 or9 n==10 or n==12 or n==13 or n==14 or n==15 or n==17 or n==18:
                lookup[x,n]=int()"""
    """print newLookup[0]
    print lookup[0]
    """
    return lookup
    
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
    print "Threshold complete with New Length = " + str(len(connection))
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
    print "Nodes: " + str(len(nodes))
    return nodes

def concatNodeAndLookup(nodes,lookup):
    
    """print type(nodes[0])
    print lookup.iloc[0]['AIRPORT_SEQ_ID']
    print type(lookup.iloc[0]['AIRPORT_SEQ_ID'])"""
    
    thisList = []
    #n=0
    #df2 = pd.DataFrame(data = ,index = lookup.dtypes)
    #print lookup[n:n+1]
    #thisList.append(lookup[n:n+1])
    
    for x in xrange(0,len(nodes)-1):#for every node
        for n in xrange(0,len(lookup)-1):#look through lookup
            if nodes[x] == lookup.iloc[n]['AIRPORT_SEQ_ID']:
                #print lookup[n:n+1]
                thisList.append(lookup[n:n+1])
    df2 = pd.DataFrame(data = thisList ,index = lookup.dtypes)
    print df2
    """nAndL = np.empty((len(nodes),len(lookup[0])))  #numpy array to fit (n) nodes and lookup (len=15)
    
    #print "Nodes+Lookup contains: " + str(nAndL.size) + " (=" + str(len(nodes)) + "*" + str(len(lookup[0])) + ")"
    print "Nodes contains:"+ str(len(nodes)) + " " + str(type(nodes[0]))
    print "Lookup contains:"+ str(len(lookup[0])) + " " + str(type(lookup[0,0]))
    
    for n in xrange(0,len(nodes)-1):                        #for each row in nodes
        #print "Searching mate for " + str(npNodeArray[n])
        #currentNode = np.empty(15)                          #empty the iteration node
        #currentNode[0] = str(nodes[n])                      #add the next node name
        nAndL[n,0] = nodes[n]                      #add the next node name
        for l in xrange(0,len(lookup)-1):                   #search through lookup.
            #print lookup[l,0]
            #print str(currentNode[0])
            if nAndL[n,0] == lookup[l,0]:               #for the row who's lookup seqID matches the current node's seqID 
                #print "found " +  lookup[l,0]
                for x in xrange(1,15):
                    nAndL[n,x] = lookup[l,x]           #fill the currentNode with fields 1-15 of lookup
                #print "CurrentNodeLen= " + str((currentNode.size)) + "\nand nAndLLen= " + str((nAndL.size))                      #to store in the node-lookup combo"""
    print "Concatenated Nodes with their lookup"
    