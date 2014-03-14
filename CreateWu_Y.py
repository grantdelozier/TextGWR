#import sys
#sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/")
import psycopg2
import codecs
import datetime
#from itertools import chain
#import string
import math
import numpy
import io

class Person:

    userID = ""
    userLat = ""
    userLong = ""
    Feature_Freq = {}
    total_words = 0
    Feature_Prob = {}
    outside_word_prob = 0
    Feature_StdDev = {}
    fileFrom = ""

    def __init__(self, ID, latit, longit, F_Freq, file_from):
        
        self.userID = ID
        self.userLat = latit
        self.userLong = longit
        self.Feature_Freq = F_Freq
        self.fileFrom = file_from
        tw = 0
        for f in F_Freq:
            tw += int(F_Freq[f])
        self.total_words = tw

    def PrintAll(self):
        print self.userID
        print self.userLat
        print self.userLong
        print self.total_words
        print self.Feature_Prob


def BuildWuMatrix(LocId, User_Lookup, kerntype, dist, cur, ptbl, pointgrid, zeroed):
    #####Add a little bit of noise to prevent singular matrix####
    #I_M = .00001 * numpy.identity(len(User_Lookup))
    
    Wu_start_time = datetime.datetime.now()
    print "########Building W(u) matrix########"
    if kerntype == 'epanech' and zeroed == True:
        #Epanechnikov Kernel function, values past dist threshold are zeroed
        cur.execute("SELECT %s.uid, .75 * (1 - power((ST_Distance_Sphere(%s.geom, %s.coord)/%s), 2)) FROM %s, %s WHERE %s.id = %s and (ST_Distance_Sphere(%s.geom, %s.coord) < %s);" % (ptbl, pointgrid, ptbl, dist, ptbl, pointgrid, pointgrid, '%s', pointgrid, ptbl, dist), (LocId, ))
    if kerntype == 'quartic' and zeroed == True:
        #Quartic Biweight Kernel function, values past dist threshold are zeroed
        cur.execute("SELECT %s.uid, power(1 - power((ST_Distance_Sphere(%s.geom, %s.coord)/%s), 2), 2) FROM %s, %s WHERE %s.id = %s and (ST_Distance_Sphere(%s.geom, %s.coord) < %s);" % (ptbl, pointgrid, ptbl, dist, ptbl, pointgrid, pointgrid, '%s', pointgrid, ptbl, dist), (LocId, ))
    elif kerntype == 'quartic' and zeroed == False:
        #Quartic Biweight Kernel function, values past dist threshold will not be zeroed
        cur.execute("SELECT %s.uid, power(1 - power((ST_Distance_Sphere(%s.geom, %s.coord)/%s), 2), 2) FROM %s, %s WHERE %s.id = %s;" % (ptbl, pointgrid, ptbl, dist, ptbl, pointgrid, pointgrid, '%s'), (LocId, ))
    Wu_Matrix = numpy.zeros( (len(User_Lookup), 1) )
    for row in cur.fetchall():
        Wu_Matrix[User_Lookup[row[0]]][0] = row[1]
    Wu_end_time = datetime.datetime.now()
    print "######Finished Building W(u) matrix#######"
    print Wu_end_time - Wu_start_time
    return Wu_Matrix

def BuildYVector(LocId, User_Lookup, cur, ptbl, pointgrid):
    print "#####Building Y Vector######"
    #Y_start_time = datetime.datetime.now()
    Y_V = numpy.zeros( (len(User_Lookup), 1) )
    cur.execute("SELECT %s.uid, ST_Distance_Sphere(%s.geom, %s.coord)/1000 FROM %s, %s WHERE %s.id = %s;" % (ptbl, pointgrid, ptbl, pointgrid, ptbl, pointgrid, '%s'), (LocId, ))
    for row in cur.fetchall():
        Y_V[User_Lookup[row[0]]][0] = row[1]
    #Y_end_time = datetime.datetime.now()
    print "######Finished Building Y matrix#######"
    #print Y_end_time - Y_start_time
    return Y_V

def WriteMatrices(W, Y, u, folderpath, kerntype):
    print "Beginning W, Y Write to file"
    wf = open(folderpath + str(u)+ "_" + kerntype +"_WUVECTOR.bin", 'w')
    #for r in W:
    #    wf.write(str(r[0]) + '\r\n')
    numpy.save(wf, W)
    wf.close()
    yf = open(folderpath + str(u)+"_YVECTOR.bin", 'w')
    #for r in Y:
    #    yf.write(str(r[0]) + '\r\n')
    numpy.save(yf, Y)
    yf.close()



def create(w_y_direct, ulist, kerntype, dist, conn_info, ptbl, pointgrid, zeroed, rf_obs_in):
    print "Successful Import"

    #Connecting to Database
    conn = psycopg2.connect(conn_info)
    print "Connecton Success"

    cur = conn.cursor()
    
    URef = {}
    with codecs.open(rf_obs_in, 'r', encoding='utf-8') as w:
        for line in w:
            row = line.strip().split('\t')
            URef[row[0]] = int(row[1])

    print "Number Obs Loaded: ", len(URef)
    
    for u in ulist:
        print "-------", str(u), "---------"
        
        build_start = datetime.datetime.now()

        W_M = BuildWuMatrix(u, URef, kerntype, dist, cur, ptbl, pointgrid, zeroed)
        Y = BuildYVector(u, URef, cur, ptbl, pointgrid)       
        WriteMatrices(W_M, Y, u, w_y_direct, kerntype)
        
        build_end = datetime.datetime.now()           
        print "Time Elapsed: ", (build_end - build_start)
        
    conn.close()
