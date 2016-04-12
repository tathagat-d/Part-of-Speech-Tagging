#!/usr/bin/python

# USE HMM MODEL FROM hmmlearn.py TO TAG UNKNOWN DATA
import json
import sys

fname  = sys.argv[1]
output = 'hmmoutput.txt'
# Getting the learned model from the output file. hmmmodel.txt
#============================================================================== 
with open('hmmmodel.txt') as f:
    data = json.load(f)
#freqTags   = data['TAG']
#freqTrans  = data['TRANSITION']
Emission   = data['Emission']
Transition = data['Transition']

#============================================================================== 
def tracePath(s, line, T, B):
    for t in range(T, 0, -1):
        line[t - 1] =  line[t - 1] + '/' + s
        s = B[s][t]
    line = ' '.join(line)
    return line

#==============================================================================
def viterbi(line):
    if not line: return
    line = line.split()
    T    = len(line)
    length = T
    P    = dict()
    B    = dict()
    #==========================================================================e
    # Initialization step at t = 1
    for tag in Transition:
        if tag == 'start': continue
        P[tag] = dict()
        B[tag] = dict()
        try:
            P[tag][1] = Emission[line[0]][tag] * Transition['start'][tag]
            B[tag][1] = 'start'
        except KeyError:
            # KeyError is for absense of OBSERVATION for current tag
            P[tag][1] = 0
    #==========================================================================
    # Recursion step for the remaining time points
    for t in range(1, T):
        word = line[t]
        for tag in Transition:
            if tag == 'start': continue
            #==================================================================
            P[tag][t+1] = 0
            # Unknown Word. Ignore Observation.(This should be in outside loop)
            if not word in Emission:
                b = 1
            else:
                # Word exists. But does it exists for current tag?
                if tag in Emission[word]:
                    b = Emission[word][tag]
                else:
                    continue
            #==========================================================
            for var in Transition:
                if var == 'start': continue
                if P[var][t] == 0:
                    temp = 0
                else:
                    temp = P[var][t] * Transition[var][tag] * b

                if not P[tag][t+1] or P[tag][t+1] < temp:
                    P[tag][t+1] = temp
                    B[tag][t+1] = var
            #==================================================================
    # End of outermost for loop
    #==========================================================================
    # Termination Step
    mps = None
    most_probable_state = None
    for tag in P:
        if not mps or mps < P[tag][length]:
            mps = P[tag][length]
            most_probable_state = tag
    #==========================================================================
    return tracePath(most_probable_state, line, T, B)

#============================================================================== 
#Reading files from the test data one line at a time
fhand = open(fname, 'r')
for line in fhand:
    line = line.strip().decode('utf-8')
    line  = viterbi(line)
    print line
fhand.close()

#==============================================================================
