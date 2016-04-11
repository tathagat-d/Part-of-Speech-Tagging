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
def viterbi(line):
    line = line.split()
    T    = len(line)
    #==========================================================================e
    # Initialization step at t = 1
    for tag in freqTags:
        P[tag] = dict()
        B[tag] = dict()
        B[tag][1] = 'start'
        try:
            P[tag][1] = float(Transition['start'][tag])/freqTrans['start']
        except KeyError:
            P[tag][1] = 0
    #==========================================================================
    # Recursion step for the remaining time points
    for t in range(T):
        print line[t]
        # tag = q(current state)
        for tag in freqTags:
            #print t + 2
            P[tag][t+2] = max(1, 2)
            B[tag][t+2] = max(1, 2)
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
