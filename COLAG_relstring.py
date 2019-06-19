#creates relstring for python to use in yang VL



def setupRel():
    sentence_file = "COLAG_2011_sents.txt" #reads in sentfile which contains [ID] [ILLOC] [SENT]
    relFile = {} #empty dictionary to hold relevance string
    File = open(sentence_file, "r")
    for line in File:
        line = line.rstrip()
        # grab the ID's - all are int's so map works
        [sentID, illoc, sent] = line.split("\t")
        #add all sentID as key to dictionary, value is list of 1's (all parameters relevant)
        relFile[sentID] = [1,1,1,1,1,1,1,1,1,1,1,1,1]
        #if Preposition is not the sentence, the Prep parameter [7] is irrelevant -1
        if "P" not in sent:
            relFile[sentID][7]= -1
            print(sent, relFile[sentID])
    return(relFile) # returns Dictionary where {sentID:[list containing 1, except for PS (-1 or 1)]


SENTENCES = setupRel() #dictionary with list of rel

