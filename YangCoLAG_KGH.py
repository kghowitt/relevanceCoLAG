#This version of Yang CoLAG was modified by KGH and WM on 6/5/2019 for the Irrelevance and Ambiguity project
#Frequency and Batch functionality was removed; earlier version can be found on WM google drive shared by CY. 

# 1)    set all elements of Wcurr to .5
# 2)    Gcurr = chooseBasedOn(Wcurr)
# 3)    s = penalty (Gcurr, Gtarg)
# 4)    based on s, make a random decision if Gcurr can parse s
# 5)    if Gcurr can parse s, Wcurr = reward(Wcurr) else Wcurr = punish(Wcurr)
# 6)    if all weights fall within threshold t, output number of sentences and exit
# 7)    goto 2)

from collections import defaultdict
import random

##########
# Globals - Note "grammars" and "sentences" are globally stored as integer "ids"
##########    except for Gtarg, and Gcurr (see below)

LD = defaultdict(set) # the Language Domain
                       # key = grammar, value = list of sentences licensed by the grammar
                       # !!! the list of sentences should be a dict for efficient lookup !!!
                        
LD_File = "COLAG_2011_ids.txt"
# The CoLAG Domain, 3 columns, Grammar ID, Sent ID and Structure ID

Out_Data_File = "OUTDATA.csv"


n = 13 # number of parameters
r = .0005  # learning rate
trials = 10  # number of simulated learning trials to run
max_sents =  500000 # max number of sents before ending a trial
threshold = .02 # when all weights are within a threshold, stop
Wcurr = [] # current weights
Gcurr = [] # current grammar list of 1s and 0s
Gtarg = [] # target grammar list of 1s and 0s
GcurrID = -1 #decimal value of Gcurr
                      
#KGH to edit for all 3072
# set target grammar equal to CoLAG English
Gtarg = [0,0,0,1,0,0,1,1,0,0,0,1,1]
GtargID = int("0001001100011",2)

Ltarg = [] # list os sentences licensed by Gtarg

##############
# END Globals
##############


##########################
# Global Functions
##########################
def setupLD() :
  File = open(LD_File,"r")
  for line in File:
    line = line.rstrip()
    # grab the ID's - all are int's so map works
    [grammID, sentID, structID] = map(int, line.split("\t")) 
    # add grammID as key, append sentID to the list of sentences (ignore structID)
    global LD
    LD[grammID].add(sentID)
    
def setupLtarg() : 
  global Ltarg
  Ltarg = list(LD[GtargID]) # use Python set to remove duplicates
                                 #  due to within language ambiguity

def reward(s) :  # CHECK
  global Wcurr, Gcurr
  for i in range(n):
    if relevant(s,n): #needs to be defined
        if Gcurr[i]==0:
          Wcurr[i] -= r*Wcurr[i];
        else:
          Wcurr[i] += r*(1.0-Wcurr[i]);

def relevant(s,n):
    #assumes SENTENCES is a global dictionary with key: sentID and value: list of -1(irr.) or 1(rel.)
    if SENTENCES[s][n] = 1:
        return True
    else:
        return False

def punish() : # CHECK
  global Wcurr, Gcurr
  for i in range(n):
    if Gcurr[i]==0:
      Wcurr[i] += r*(1.0-Wcurr[i]);
    else:
      Wcurr[i] -= r*Wcurr[i];

def converged():
  #if GcurrID in {611, 99, 547, 227, 867, 35, 163, 803, 99}: #superset and equivalent languages
  #    return True 
      
  for i in range(n):
    if i not in [3,6]: #considered convergence when all parameters except OPT(3) and WHM(6) converge becayse they never reach threshold
        if not (1-Wcurr[i] <  threshold  or Wcurr[i] < threshold): 
          return False
  return True

def canParse(s,l): # is sentence s in language l
  if s in l:  # l is set, so membership is more efficient than list
    return True
  else:
    return False
  
def chooseGrammarBasedOn(weights):
    Gtmp =[]
    for i in range(n):
        x = random.random()
        if x < weights[i]: # checked against Charles code
            Gtmp.append(1)
        else:
            Gtmp.append(0)
        
    return Gtmp
  
def chooseSentUnif():  
#UNIFORM
    x = random.randint(0,len(Ltarg)-1)
    sID = Ltarg[x]

    return sID


def bin2Dec(bList): # bList is a list of 1's and 0's
    binStr = ""
    for b in bList:
        binStr += str(b)
    return int(binStr,2)     
    
    
    
def csvOutput(File, run, cnt, G, W):
    Gout =""
    Wout =""
    for i in range(n):
      Gout += str(G[i])
    for i in range(n):
      Wout += str(round(W[i],15))+","

    outStr = str(run)+","+str(cnt)+","+str(bin2Dec(G))+","+"'"+Gout+","+Wout+"\n"
    File.write(outStr)
  
############################################
## MAIN MAIN MAIN reward only learner
############################################
print("Setting up ...")
setupLD()
setupLtarg()

OUTDATA = open(Out_Data_File,"w")

Gs = LD.keys() # a list of all valid CoLAG grammar IDs
# Convert list into a dictionary, 
# a dictionary of CoLAG Grammars - value of 0 is a dummy value;
#   a dictionary is used for efficient  lookup.
CoLAG_Gs = {}
for g in Gs:
    CoLAG_Gs[g]=0

print("Running ...")

for runNum in range(trials):
  
  Wcurr = [.5 for i in range(n)] # initialize weights to 0.5
  Gcurr = [-1]
  GcurrID = bin2Dec(Gcurr)
  numSents = 0
  b = 0

  while not converged() and numSents < max_sents:

      Gcurr = chooseGrammarBasedOn(Wcurr)
      GcurrID = bin2Dec(Gcurr)
      while GcurrID not in CoLAG_Gs:
           Gcurr = chooseGrammarBasedOn(Wcurr)
           GcurrID=bin2Dec(Gcurr)

      s = chooseSentUnif()
      
      numSents = numSents + 1
     
      if canParse(s,LD[GcurrID]):
          reward()

      #sentID 13 y/n for rel
      #for i in n:
      #    if sentID[i] == y:
      #      reward Wcurr[i]
      #
      #ah
          
      #if numSents > (max_sents - 10):
      #    csvOutput(OUTDATA, runNum, numSents, Gcurr , Wcurr)      

  if runNum % 1 == 0:
    print("RUN: ", runNum)


  csvOutput(OUTDATA, runNum, numSents, Gcurr , Wcurr)      

    
OUTDATA.close()

print("Done.")
