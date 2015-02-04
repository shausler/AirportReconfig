import community
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np

connection = np.zeros((0,6)) #unique values
#node = np.zeros(500)
rownum = 0
numswapped = 0
#rownum = -1 # so it starts at 0 (only for testing)

"""#Column meanings
    0"YEAR",
    1"ORIGIN_AIRPORT_ID",
    2"DEST_AIRPORT_ID",
    3"PASSENGERS",
    4"DISTANCE",
    5"NUM_OF_FLIGHTS",
"""

#read in csv
csvfile = open("files\\10.csv","rb")    #open your file
dialect = csv.Sniffer().sniff(csvfile.read(1024)) #find the dialect
csvfile.seek(0)
reader = csv.reader(csvfile, dialect) #read the file, under the dialect
for row in reader: #for each row
    rownum+=1
    #print rownum #+ str(row)
    if(row[1]>row[2]): #if not least to most
        swapper = row[1]
        row[1] = row[2] #make first number least 
        row[2] = swapper # and second number most
        numswapped+=1
        #print "Swapped " + str(rownum)
        
    srcloc = np.where(connection[:,1]==int(row[1]))[0]     #where did we find the first node?
    destloc = np.where(connection[:,2]==int(row[2]))[0]     #where did we find the second node?
        
    if(np.any(srcloc==destloc)): # Both in there
        #print "Both in there at " + str(srcloc) + " & " + str(destloc)
        connection[np.where(srcloc==destloc)[0], 5]+=1      #add to the number of flights recorded
        connection[np.where(srcloc==destloc)[0], 3] += float(row[3])                      #add passengers up
        
        """elif(np.any(srcloc==destloc) and row[1] != row[2]): # Only the first occurred, so add
        print "Only the first occurred at " + str(srcloc) + " & " + str(destloc)
        n = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]
        myRow = np.array([n])
        connection = np.vstack((connection,myRow))
        numTF+=1"""
        
    else: #Neither in there, so add
        #print "Neither in there"
        #n = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]
        #print n
        myRow = np.array([[float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(1)]])
        connection = np.vstack((connection,myRow))
        
#    print ""
print len(connection)
print str(connection)
#print str(numTF) + " " + str(numFF)
np.save("files\\npArrayFlights1.txt", connection)

"""#Community Partitions
#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure

G = nx.erdos_renyi_graph(100, 0.04)

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))
print partition

nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()
"""

"""#Query np array
connection1 = np.zeros((10,6)) #up to 20 cells
connection1[rownum,2]=4
connection1[rownum,5]=1
rownum+=1
connection1[rownum,1]=1
connection1[rownum,2]=5
connection1[rownum,5]=1
rownum+=1
connection1[rownum,1]=2
connection1[rownum,2]=4
connection1[rownum,5]=1
rownum+=1
#print "Empty = " + str(np.empty([2,2]))#    
#print "Node found? " + str(np.where(node==123)[0])#             where 122 occurs
#print "length? " + str(len(np.where(node==123)[0]))#            number of times 122 occurs 
#print "Connection found? " + str(np.where(connection==10397)[0])
src = 0
dest = 4
srcloc = np.where(connection1[:,1]==src)[0]     #where did we find the first node?
destloc = np.where(connection1[:,2]==dest)[0]     #where did we find the second node?
print "Column 1:" + str(connection1[:,1])
print "Column 2:" + str(connection1[:,2])
print srcloc     #location of source
print destloc     #location of dest
print "Are there any perfect matches? " + str(np.any(srcloc==destloc))     #does this cell have both?
if(not np.any(srcloc==destloc) and src != dest):
    print "Was only the first existing? " + str(np.any(destloc))
"""

"""#Small-scale np array load
connection1 = np.zeros((10,6)) #up to 20 cells
connection1[rownum,1]=1
connection1[rownum,2]=4
connection1[rownum,5]=1
rownum+=1
connection1[rownum,1]=1
connection1[rownum,2]=5
connection1[rownum,5]=1
rownum+=1
connection1[rownum,1]=2
connection1[rownum,2]=4
connection1[rownum,5]=1
rownum+=1
src = 1 #look thru all 1s
dest = 4 #paired with 3 to 10
x=dest
while(x <= 10): #for thru x thru 10
    print str(src) + " " + str(dest)
    srcloc = np.where(connection1[:,1]==src)[0]     #where did we find the first node?
    destloc = np.where(connection1[:,2]==dest)[0]     #where did we find the second node?
    
    #print "Are there any perfect matches? " + str(np.any(srcloc==destloc)) + ". If so, where? " + str(np.where(srcloc==destloc)[0])
    if(np.any(srcloc==destloc)): # Both in there
        print "Both in there at " + str(srcloc) + " & " + str(destloc)
        connection1[np.where(srcloc==destloc)[0], 5]+=1
        
    elif(not not np.any(srcloc==destloc) and src != dest):# Only the first occurred, so add
        print "Only the first occurred at " + str(srcloc) + " & " + str(destloc)
        connection1[rownum, 1]=src
        connection1[rownum, 2]=dest
        connection1[rownum, 5]=1
        rownum+=1
        
    else: #Neither in there, so add
        print "Neither in there"
        connection1[rownum, 1]=src
        connection1[rownum, 2]=dest
        connection1[rownum, 5]=1
        rownum+=1
    print " "
    dest+=1
    x+=1
print connection1
"""