import codecs
import datetime
from itertools import chain
#import numpy
import io
import math

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
        if method == "likelihood":
            for word in F_Freq:
                F_Prob[word] = (float(F_Freq[word]) / (float(self.total_words)))
                #print "####Actual Word#####"
                #print F_Prob[word]
            self.outside_word_prob = 0.0                                   

        self.Feature_Prob = F_Prob

def ModeCalc_2(F_All, personList, NumPeople, rf_obs_out, rf_std_out):
    print "Starting Calculation of mean probability"
    j = 0
    wordDict = {}
    start_mean = datetime.datetime.now()
    for word in F_All:
        for person in personList:
            if word in wordDict:
                if word in person.Feature_Prob:
                    wordDict[word] += person.Feature_Prob[word]
                else:
                    wordDict[word] += person.outside_word_prob
            else:
                if word in person.Feature_Prob:
                    wordDict[word] = person.Feature_Prob[word]
                else:
                    wordDict[word] = person.outside_word_prob
        j += 1
        if j % 5000 == 0:
            print j
            print datetime.datetime.now()

    print "Total Mean Calc Time:"
    print datetime.datetime.now() - start_mean

    obs_ref_file = codecs.open(rf_obs_out, 'w', encoding='utf-8')

    
    j = 0
    wordStds = {}
    print "Starting Std Dev Calculations"
    start_mean = datetime.datetime.now()
    z = 0
    for person in personList:
        obs_ref_file.write((person.userID).encode('utf-8').decode('utf-8') + '\t' + str(z) + '\r\n')
        z += 1
        for word in wordDict:
            if j == 0:
                wordDict[word] = float(wordDict[word]) / float(NumPeople)
                if word in person.Feature_Prob:
                    wordStds[word] = math.pow((person.Feature_Prob[word] - wordDict[word]), 2)
                else:
                    wordStds[word] = math.pow((float(person.outside_word_prob) - wordDict[word]), 2)
            else:
                if word in person.Feature_Prob:
                    wordStds[word] += math.pow((float(person.Feature_Prob[word]) - wordDict[word]), 2)
                else:
                    wordStds[word] += math.pow((float(person.outside_word_prob) - wordDict[word]), 2)
        j += 1
        if j % 5000 == 0:
            print j
            print datetime.datetime.now()

    obs_ref_file.close()

    std_dev_outfile = codecs.open(rf_std_out, 'w', encoding='utf-8')

    print "Number words in model:", len(wordStds)

    for i in wordStds:
        try:
            std_dev_outfile.write((i.encode('utf-8').decode('utf-8') + '\t' + str(wordDict[i]) + '\t' + str(math.sqrt(wordStds[i]/float(NumPeople))) + '\r\n'))
        except:
            print i, type(i)
            print "Broken word: ", i
        
    std_dev_outfile.close()

    print "Total Std Dev Time: ", start_mean - datetime.datetime.now() 

def ModeCalc_1(F_All, personList, NumPeople, rf_obs_out, rf_std_out):
    print "Starting Calculation of mean probability"
    j = 0
    wordDict = {}
    start_mean = datetime.datetime.now()
    for person in personList:
        for word in F_All:
            if j == 0:
                if word in person.Feature_Prob:
                    wordDict[word] = person.Feature_Prob[word]
                else:
                    wordDict[word] = person.outside_word_prob
            else:
                if word in person.Feature_Prob:
                    wordDict[word] += person.Feature_Prob[word]
                else:
                    wordDict[word] += person.outside_word_prob
        j += 1
        if j % 5000 == 0:
            print j
            print datetime.datetime.now()

    print "Total Mean Calc Time:"
    print datetime.datetime.now() - start_mean

    obs_ref_file = codecs.open(rf_obs_out, 'w', encoding='utf-8')

    
    j = 0
    wordStds = {}
    print "Starting Std Dev Calculations"
    start_mean = datetime.datetime.now()
    z = 0
    for person in personList:
        obs_ref_file.write((person.userID).encode('utf-8').decode('utf-8') + '\t' + str(z) + '\r\n')
        z += 1
        for word in wordDict:
            if j == 0:
                wordDict[word] = float(wordDict[word]) / float(NumPeople)
                if word in person.Feature_Prob:
                    wordStds[word] = math.pow((person.Feature_Prob[word] - wordDict[word]), 2)
                else:
                    wordStds[word] = math.pow((float(person.outside_word_prob) - wordDict[word]), 2)
            else:
                if word in person.Feature_Prob:
                    wordStds[word] += math.pow((float(person.Feature_Prob[word]) - wordDict[word]), 2)
                else:
                    wordStds[word] += math.pow((float(person.outside_word_prob) - wordDict[word]), 2)
        j += 1
        if j % 5000 == 0:
            print j
            print datetime.datetime.now()

    obs_ref_file.close()

    std_dev_outfile = codecs.open(rf_std_out, 'w', encoding='utf-8')

    print "Number words in model:", len(wordStds)

    for i in wordStds:
        try:
            std_dev_outfile.write((i.encode('utf-8').decode('utf-8') + '\t' + str(wordDict[i]) + '\t' + str(math.sqrt(wordStds[i]/float(NumPeople))) + '\r\n'))
        except:
            print i, type(i)
            print "Broken word: ", i
        
    std_dev_outfile.close()

    print "Total Std Dev Time: ", start_mean - datetime.datetime.now() 


def GetWords(wordlist):
    Words_List = []
    print "Reading Word List"
    with io.open(wordlist, 'r', encoding='utf-8') as w:
        for line in w:
            if line.strip() not in Words_List:
                Words_List.append(line.strip())

    print "Word List Length:", len(Words_List)
    return Words_List

#This version only includes words that appear in both the wordlist and somewhere in the data
def GetWords2(wordlist, allwords):
    Words_List = []
    print "Reading Word List"
    with io.open(wordlist, 'r', encoding='utf-8') as w:
        for line in w:
            if line.strip() not in Words_List and line.strip() in allwords:
                Words_List.append(line.strip())

    print "Word List Length:", len(Words_List)
    return Words_List

def Build_ref_files(tf, rf_std_out, rf_obs_out, wordlist, listuse):
    print "Success Importing"
    trainFile = tf
    
    #openTrain = codecs.open(trainFile, 'r', encoding='utf-8')
    filename = trainFile[trainFile.rfind('/')+1:]
    print filename
    begin_time = datetime.datetime.now()
    personList = []
    
    y = 0

    F_All = {}

    if listuse == 'restricted':
        F_All = set()
        with io.open(wordlist, 'r', encoding='utf-8') as w:
            whitelist = set([x.strip() for x in w])
            
    print len(whitelist)

    
    #The length given here was observed from a smaller corpus of about 6000 people
    F_All_Len = 114616

    read_time_begin = datetime.datetime.now()
    z = 0
    x = 0
    
    with io.open(trainFile, 'r', encoding='utf-8') as f:
        for person in f:
            x += 1
            #print "####NEW Person####"
            #print userID, latit, longit
            try:
                row = person.strip().split('\t')
                #print row[0]
                userID = row[0]
                latit = row[1].split(',')[0]
                longit = row[1].split(',')[1]
                F_Freq = dict(f.strip().split(':') for f in row[2].split(" "))
                if wordlist == 'any':
                    F_All = dict(chain(F_Freq.iteritems(), F_All.iteritems()))
                if listuse == 'restricted':
                    #F_All = set()
                    F_All |= set([j for j in F_Freq if j in whitelist])
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
    print "Calculating Prob"

    print "------Done reading in the data-------"
    read_time_end = datetime.datetime.now()
    print read_time_end - read_time_begin


    if wordlist != 'any' and listuse == 'all':
        F_All = GetWords(wordlist)
    elif wordlist != 'any' and listuse == 'restricted':
        F_All = GetWords2(wordlist, F_All)

    NumPeople = len(personList)

    print "Num Obs: ", NumPeople
    print "Num Vars: ", len(F_All)
    
    if NumPeople > len(F_All):
        print "Starting on Mode 1 (More Observations Than Variables)"
        ModeCalc_1(F_All, personList, NumPeople, rf_obs_out, rf_std_out)
    else:
        print "Starting on Mode 2 (More Variables Than Observations)"
        ModeCalc_2(F_All, personList, NumPeople, rf_obs_out, rf_std_out)

    print "Done Writing Std Dev File"

