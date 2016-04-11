#!/usr/bin/python

# USE HMM MODEL FROM hmmlearn.py TO TAG UNKNOWN DATA
import json
import sys

fname  = sys.argv[1]
output = 'hmmoutput.txt'
P      = dict()
B      = dict()
# Getting the learned model from the output file. hmmmodel.txt
#============================================================================== 
with open('hmmmodel.txt') as f:
    data = json.load(f)
freqTags   = data['TAG']
freqTrans  = data['TRANSITION']
Emission   = data['Emission']
Transition = data['Transition']

#============================================================================== 
def computeProbability(t, tag, word):
    r1 = list()
    r2 = list()
    for var in freqTags:
        try:
            transition = float(Transition[var][tag])/freqTrans[var]
            emission   = float(Emission[tag][word])/freqTags[tag]
            r1.append(P[var][t] * transition * emission)
            r2.append((P[var][t] * transition, var))
        except KeyError:
            r1.append(0)
            r2.append((0, var))
    return max(r1), max(r2)[1]

#==============================================================================
def viterbi(line):
    if not line: return
    line = line.split()
    T    = len(line)
    #==========================================================================e
    # Initialization step at t = 1
    for tag in freqTags:
        P[tag] = dict()
        B[tag] = dict()
        B[tag][1] = 'start'
        try:
            transition = float(Transition['start'][tag])/freqTrans['start']
            emission   = float(Emission[tag][line[0]])/freqTags[tag]
            P[tag][1] = transition * emission
        except KeyError:
            P[tag][1] = 0
    #==========================================================================
    # Recursion step for the remaining time points
    for t in range(1, T):
        for tag in freqTags:
            P[tag][t+1], B[tag][t+1] = computeProbability(t, tag, line[t])
    #==========================================================================
    # Termination Step
    # Some code to follow up here

#============================================================================== 
#Reading files from the test data one line at a time
fhand = open(fname, 'r')
for line in fhand:
    line = line.strip()
    viterbi(line)

'''
for tag in P:
    print tag , P[tag]
for tag in B:
    print tag , B[tag]
'''
#==============================================================================
