import psycopg2
import datetime
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

def Load(tf, tbl_name, conn_info):

    #Connecting to Database
    conn = psycopg2.connect(conn_info)
    print "DB Connection Success"

    trainFile = tf
    
    #openTrain = codecs.open(trainFile, 'r', encoding='utf-8')
    filename = trainFile[trainFile.rfind('/')+1:]
    print filename
    begin_time = datetime.datetime.now()
    personList = []
    x = 0
    y = 0

    #The length given here was observed from a smaller corpus of about 6000 people
    F_All_Len = 114616

    read_time_begin = datetime.datetime.now()
    z = 0
    
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
                F_Freq = dict(f.split(':') for f in row[2].split(" "))
                #F_All = dict(chain(F_Freq.iteritems(), F_All.iteritems()))
                #print len(F_Freq)
                #F_Freq = {}
                newPerson = Person(userID, latit, longit, F_Freq, filename)
                #newPerson.CalcProb('smoothed', 30, False, F_All_Len)
                personList.append(newPerson)
            except:
                print "@@@@@error reading user@@@@@@"
                print row
                print z
                #break
            z += 1
            if z % 5000 == 0:
                print z
                print datetime.datetime.now()


    print "------Done reading in the data-------"
    read_time_end = datetime.datetime.now()
    print read_time_end - read_time_begin

    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS %s (uid varchar(20) primary key, latit float, longit float, total_words integer, coord geometry(Point, 4326), filefrom varchar(50));" % (tbl_name, ))

    cur.execute("DELETE FROM %s" % tbl_name)
   
    for p in personList:
        SQL1 = "INSERT INTO %s VALUES (%s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)', 4326), %s);" % (tbl_name, '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        data = (p.userID, float(p.userLat), float(p.userLong), p.total_words, float(p.userLong), float(p.userLat), p.fileFrom)
        cur.execute(SQL1, data)

    conn.commit()
    conn.close()

    print "Number of people loaded: ", len(personList)

    print "Done Loading ", tbl_name
    
    
