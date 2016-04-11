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
freqTags   = data['TAG']
freqTrans  = data['TRANSITION']
Emission   = data['Emission']
Transition = data['Transition']
#============================================================================== 
def viterbi(line):
    line = line.split()
    for tag in freqTags:
        try:
            print float(Transition['start'][tag])/freqTrans['start'], 'start', tag 
        except KeyError:
            print 0, 'start', tag
#============================================================================== 
#Reading files from the test data one line at a time
fhand = open(fname, 'r')
for line in fhand:
    line = line.strip()
    viterbi(line)
