import numpy
import io
import datetime
import math
import codecs

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


def GetStdDevRef(ref_file):
    Std_dev_reference = {}
    i = 0
    with io.open(ref_file, 'r', encoding='utf-8') as f:
        for line in f:
            row = line.strip().split('\t')
            if len(row) >= 3:
                Std_dev_reference[row[0]] = (i, float(row[1]), float(row[2]))
                i += 1
            else: print "Something wrong with this row:", row
    return Std_dev_reference

def BuildInputVector(person, std_dev_ref):
    I_V = numpy.zeros( (1, len(std_dev_ref)) )
    for word in std_dev_ref:
        if word in person.Feature_Prob:
            zscore = float(person.Feature_Prob[word] - std_dev_ref[word][1]) / float(std_dev_ref[word][2])
            #if zscore > 2.0:
            #    print "High Z score word found for ", person.userID, word, zscore
            I_V[0][std_dev_ref[word][0]] = zscore
        else:
            try:
                zscore = float(person.outside_word_prob - std_dev_ref[word][1]) / float(std_dev_ref[word][2])
                I_V[0][std_dev_ref[word][0]] = zscore
            except:
                print "Problem reading"
                print word
                
    return I_V

#Read in B Vectors
def GetBVector(u, directory, kerntype):
    thefile = open(directory + 'Bu_' + str(u) + "_" + kerntype + ".bin", 'rb')
    B_V = numpy.load(thefile)
    return B_V

#Multiply, write to file
def WritePrediction(uid_dict, u):
    w_file = codecs.open("GWR_TEST_quarticzeroed_lam10_Predictions.txt", 'a', encoding='utf-8')
    for uid in uid_dict:
        w_file.write(str(uid).encode('utf-8') + '\t' + str(u).encode('utf-8') + '\t' + str(uid_dict[uid][0][0]).encode('utf-8') + '\r\n')
    w_file.close()

def test(f, std_ref, bu_direct, ulist, kerntype):
    
    #openTrain = codecs.open(trainFile, 'r', encoding='utf-8')
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

    std_dev_reference = GetStdDevRef(std_ref)
    for u in ulist:
        print u
        B_V = GetBVector(u, bu_direct, kerntype)
        uid_dict = {}
        for p in personList:            
            I_V = BuildInputVector(p, std_dev_reference)
            uid_dict[p.userID] = numpy.dot(I_V, B_V)
        WritePrediction(uid_dict, u)
    print "Done"
