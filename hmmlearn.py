#!/usr/bin/python
# LEARNING HIDDEN MARKOV MODEL FROM TRAINING DATA.
import sys
fname  = sys.argv[1]
output = 'hmmmodel.txt'
START  = 'start'
freqTags   = dict()
Emission   = dict()
freqTrans  = dict()
Transition = dict()

#==============================================================================
def getEmission(tag, word):
    if not tag in Emission:
        Emission[tag] = dict()
    if not word in Emission[tag]:
        Emission[tag][word] = 1
    else:
        Emission[tag][word] += 1

#==============================================================================
def getTransition(prevPointer, tag):
    if not prevPointer in Transition:
        Transition[prevPointer] = dict()
    if not tag in Transition[prevPointer]:
        Transition[prevPointer][tag] = 1
    else:
        Transition[prevPointer][tag] += 1

#==============================================================================
def getModel():
    fhand = open(fname, 'r')
    for line in fhand:
        line = line.strip().decode('utf-8').split()
        prevPointer = START
        for word in line:
            word = word.split('/')
            tag = word[-1]
            word = '/'.join(word[:-1])
            #===================================================================
            #Emission Probability
            freqTags[tag]   = freqTags.get(tag, 0) + 1
            getEmission(tag, word)
            #===================================================================
            #Transition Probability
            freqTrans[prevPointer]  = freqTrans.get(prevPointer, 0) + 1
            getTransition(prevPointer, tag)
            # Updating the prevPointer to current tag
            prevPointer = tag
            #===================================================================
        #End of word in line
    # End of line in fhand
    fhand.close()

#==============================================================================
def main():
    getModel()

#==============================================================================
if __name__ == '__main__':
    main()

#==============================================================================
