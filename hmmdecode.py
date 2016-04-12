#!/usr/bin/python

# USE HMM MODEL FROM hmmlearn.py TO TAG UNKNOWN DATA
import json
import sys
import math

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
        B[tag][1] = 'start'
        if not line[0] in Emission:
            P[tag][1] = math.log(Transition['start'][tag])
        elif tag in Emission[line[0]]:
            P[tag][1] = math.log(Emission[line[0]][tag]) + \
                        math.log(Transition['start'][tag])
        else:
            P[tag][1] = math.log(2.2250738585072014e-308)
    #==========================================================================
    # Recursion step for the remaining time points
    for t in range(1, T):
        word = line[t]
        for tag in Transition:
            if tag == 'start': continue
            #==================================================================
            P[tag][t+1] = math.log(2.2250738585072014e-308)
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
                if P[var][t] == math.log(2.2250738585072014e-308):
                    temp = math.log(2.2250738585072014e-308)
                else:
                    temp = P[var][t] + \
                    math.log(Transition[var][tag]) * math.log(b)

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
outputf = open('hmmoutput.txt', 'w')
for line in fhand:
    line = line.strip().decode('utf-8', 'ignore')
    line = viterbi(line)
    line = line.encode('utf-8', 'ignore')
    outputf.write(line)
    outputf.write('\n')
fhand.close()
outputf.close()

#==============================================================================
