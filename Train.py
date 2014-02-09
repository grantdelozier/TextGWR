import codecs
import datetime
#from itertools import chain
#import string
import math
import numpy
import io
import scipy.sparse as sp
from numpy.linalg import inv

class Person:

    userID = ""
    userLat = ""
    userLong = ""
    #Feature_Freq = {}
    total_words = 0
    Feature_Prob = {}
    outside_word_prob = 0
    fileFrom = ""

    def __init__(self, ID, latit, longit, F_Freq, file_from, F_All_Len):
        #self.userID = ID[ID.rfind("_")+1:]
        self.userID = ID
        self.userLat = latit
        self.userLong = longit
        #self.Feature_Freq = F_Freq
        self.fileFrom = file_from
        tw = 0
        for f in F_Freq:
            tw += int(F_Freq[f])
        self.total_words = tw
        self.CalcProb(F_Freq, 'smoothed', 30, False, F_All_Len)
        

    def CalcProb(self, F_Freq, method="likelihood", res_prob_space = 0, logNormal = False, F_All_Len=1):
        F_Prob = {}
        if method == "smoothed" and res_prob_space > 0:
            perct1 = float(self.total_words) / float(100.0 - (res_prob_space))
            other_words_space = perct1 * res_prob_space
            for word in F_Freq:
                F_Prob[word] = (float(F_Freq[word]) / (float(self.total_words) + float(other_words_space)))
                #print "####Actual Word#####"
                #print F_Prob[word]
            self.outside_word_prob = (float(other_words_space)/(F_All_Len - len(F_Freq))) / (float(self.total_words) + float(other_words_space))                                   
            #print "#####Other Word#####"
            #print F_Prob[word]
        self.Feature_Prob = F_Prob

def BuildXMatrix(people, User_Lookup, std_dev_ref, noise_value=.000001):
    #print "Generating Noise Matrix with values from 0  to ", noise_value
    X_start_time = datetime.datetime.now()
    print "######Building X Matrix ##########"
    XMatrix = numpy.empty( (len(User_Lookup), len(std_dev_ref)) )
    g = 0
    for w in std_dev_ref:
        #noise = rand.random() * noise_value
        for p in people:
            if w in p.Feature_Prob:
                XMatrix[User_Lookup[p.userID]][std_dev_ref[w][0]] = ((p.Feature_Prob[w] - std_dev_ref[w][1]) / std_dev_ref[w][2])       
            elif w in std_dev_ref:
                XMatrix[User_Lookup[p.userID]][std_dev_ref[w][0]] = ((p.outside_word_prob - std_dev_ref[w][1]) / std_dev_ref[w][2])
    X_end_time = datetime.datetime.now()
    print "######Finished Building X Matrix ##########"
    print X_end_time - X_start_time
    return XMatrix

def LoadY(wydirect, u):
    yf = open(wydirect + u + '_YVECTOR.bin', 'rb')
    yv = numpy.load(yf)
    yf.close()
    return yv

def LoadWu(wydirect, u, kerntype, numobs):

    wf = open(wydirect + u + '_' + kerntype + "_WUVECTOR.bin", 'rb')
    wv = sp.spdiags(numpy.load(wf).transpose(), [0], numobs, numobs).tocsr()
    wf.close()
    return wv

def StoreScore(u, B, scoredirect, kerntype):
    bf = open(scoredirect + 'Bu_' + u + '_' + kerntype + '.bin', 'wb')
    numpy.save(bf, B)
    bf.close()

def UpToInv(X, W, lam, wordsize):
    Ident = numpy.identity(wordsize)
    print X.shape
    print W.shape
    print Ident.shape
    firstpart = numpy.dot((X.transpose() * W), X)
    print "First part done"
    secondpart = lam * Ident
    print "Second part done"
    i = inv(numpy.add(secondpart, firstpart))
    return i
    

def train(f, rf_obs_in, rf_std_in, wu_y_direct, ulist, kerntype, lam, scoredirect):
    print "Import Train Worked"

    filename = f[f.rfind('/')+1:]
    print filename
    begin_time = datetime.datetime.now()
    personList = []
    x = 0
    y = 0

    #The length given here was observed from a smaller corpus of about 6000 people
    F_All_Len = 114616

    read_time_begin = datetime.datetime.now()
    z = 0
    
    with io.open(f, 'r', encoding='utf-8') as f:
        for person in f:
            x += 1
            #print "####NEW Person####"
            #print userID, latit, longit
            try:
                row = person.split('\t')
                #print row[0]
                userID = row[0]
                latit = row[1].split(',')[0]
                longit = row[1].split(',')[1]
                F_Freq = dict(f.split(':') for f in row[2].split(" "))
                #F_All = dict(chain(F_Freq.iteritems(), F_All.iteritems()))
                #print len(F_Freq)
                #F_Freq = {}
                newPerson = Person(userID, latit, longit, F_Freq, filename, F_All_Len)
                #newPerson.CalcProb('smoothed', 30, False, F_All_Len)
                personList.append(newPerson)
            except:
                print "@@@@@error reading user@@@@@@"
                print row
                print z
                break
            z += 1
            if z % 5000 == 0:
                print z
                print datetime.datetime.now()

 
    URef = {}
    with codecs.open(rf_obs_in, 'r', encoding='utf-8') as w:
        for line in w:
            row = line.strip().split('\t')
            URef[row[0]] = int(row[1])

    WordRef = {}
    i = 0
    with io.open(rf_std_in, 'r', encoding='utf-8') as w:
        for line in w:
            row = line.strip().split('\t')
            if len(row) == 3:
                WordRef[row[0]] = (i, float(row[1]), float(row[2]))
                i += 1
            else: print "Problem Reading row from std ref:", row

    print "Num Obs: ", len(URef)
    print "Num Vars: ", len(WordRef)
    X_M = BuildXMatrix(personList, URef, WordRef)
    print "######X Matrix Build Complete#######"

    for u in ulist:
        print "----------",u,"-------------"
        ustart = datetime.datetime.now()
        Y_V = LoadY(wu_y_direct, u)
        Wu = LoadWu(wu_y_direct, u, kerntype, len(URef))
        Inver = UpToInv(X_M, Wu, lam, len(WordRef))
        print "Invert Finished"
        B = numpy.dot((numpy.dot(Inver, X_M.transpose()) * Wu), Y_V)
        StoreScore(u, B, scoredirect, kerntype)
        print "Total time for u"
        print datetime.datetime.now() - ustart

    print "Total Train Time: "
    print datetime.datetime.now() - read_time_begin
    
    
