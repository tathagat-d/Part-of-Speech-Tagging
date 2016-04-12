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
def tracePath(B):
    pass
#==============================================================================
def computeProbability(P, t, tag, word):
    maximum = None
    pointer = None
    try:
        b   = Emission[word][tag]
    except KeyError:
        b   = 1
    #==========================================================================e
    for var in Transition:
        if var == 'start': continue
        if P[var][t] == 0:
            temp = 0
        else:
            temp = b * P[var][t] * Transition[var][tag]

        if not maximum or maximum < temp:
            maximum = temp
            pointer = var
    #==========================================================================e
    return maximum, pointer

#==============================================================================
def viterbi(line):
    if not line: return
    line = line.split()
    T    = len(line)
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
        for tag in Transition:
            if tag == 'start': continue
            # If the previous tag was zero, its a dead path
            if P[tag][t] == 0:
                P[tag][t+1] = 0
            else:
                P[tag][t+1], B[tag][t+1] = computeProbability(P, t, tag, line[t])
    #==========================================================================
    # Termination Step
    # Some code to follow up here
    #for key, value in P.items():
    #    print key, value
    return tracePath(B)

#============================================================================== 
#Reading files from the test data one line at a time
fhand = open(fname, 'r')
for line in fhand:
    line = line.strip()
    viterbi(line)
fhand.close()

'''
for tag in P:
    print tag , P[tag]
for tag in B:
    print tag , B[tag]
'''
#==============================================================================
