#import sys
#sys.path.append("/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/")
import psycopg2
import codecs
import datetime
#from itertools import chain
#import string
import math
#import numpy
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

    def SetStdDev(self, word, std_calc):
        self.Feature_StdDev[word] = std_calc

    def PrintAll(self):
        print self.userID
        print self.userLat
        print self.userLong
        print self.total_words
        print self.Feature_Prob

    def CalcProb(self, method="likelihood", res_prob_space = 0, logNormal = False, F_All_Len=1):
        F_Prob = {}
        if method == "smoothed" and res_prob_space > 0:
            perct1 = float(self.total_words) / float(100.0 - (res_prob_space))
            other_words_space = perct1 * res_prob_space
            for word in self.Feature_Freq:
                F_Prob[word] = (float(self.Feature_Freq[word]) / (float(self.total_words) + float(other_words_space)))
                #print "####Actual Word#####"
                #print F_Prob[word]
            self.outside_word_prob = (float(other_words_space)/(F_All_Len - len(self.Feature_Freq))) / (float(self.total_words) + float(other_words_space))                                   
            #print "#####Other Word#####"
            #print F_Prob[word]
        self.Feature_Prob = F_Prob



def create(f, w_y_direct, ulist, kerntype, dist, conn_info):
    print "Successful Import"

    #Connecting to Database
    conn = pyscopg2.connect(conn_info)
    print "Connecton Success"
    
