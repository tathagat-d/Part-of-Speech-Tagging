#!/usr/bin/python
# LEARNING HIDDEN MARKOV MODEL FROM TRAINING DATA.
import sys
import json
fname  = sys.argv[1]
output = 'hmmmodel.txt'
START  = 'start'
freqTags   = dict()
Emission   = dict()
freqTrans  = dict()
Transition = dict()

#==============================================================================
def getEmission(word, tag):
    if not word in Emission:
        Emission[word] = dict()
    if not tag in Emission[word]:
        Emission[word][tag] = 1
    else:
        Emission[word][tag] += 1

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
            getEmission(word, tag)
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
# Turning Frequency into Probability
def postProcessing():
    for tag in Transition:
        for t in Transition:
            # Ignoring Start
            if t == 'start': continue
            length = len(freqTrans) - 1
            # Thats an end of line delimiter ignoring
            Transition[tag][t] = float(Transition[tag].get(t, 0) + 1) \
                    / (length + freqTrans[tag])
    #==========================================================================
    for word in Emission:
        for tag in Emission[word]:
            Emission[word][tag] = float(Emission[word][tag]) / freqTags[tag]

#==============================================================================
def main():
    getModel()
    postProcessing()
    data = dict()
    data ['Emission'] = Emission
    data ['Transition'] = Transition
    with open(output, 'w') as f:
        json.dump(data, f)
    '''
    data = dict()
    data['TAG'] = freqTags
    data['TRANSITION'] = freqTrans
    data ['Emission'] = Emission
    data ['Transition'] = Transition
    with open(output, 'w') as f:
        json.dump(data, f)
    '''

#==============================================================================
if __name__ == '__main__':
    main()

#==============================================================================
