#!/usr/bin/python
# LEARNING HIDDEN MARKOV MODEL FROM TRAINING DATA.
import sys
fname  = sys.argv[1]
output = 'hmmmodel.txt'
freqTags   = dict()
TAGS       = dict()

#==============================================================================
def getEmission():
    fhand = open(fname, 'r')
    for line in fhand:
        line = line.strip().decode('utf-8').split()
        for word in line:
            word = word.split('/')
            tag = word[-1]
            word = '/'.join(word[:-1])
            freqTags[tag]   = freqTags.get(tag, 0) + 1
            if not tag in TAGS:
                TAGS[tag] = dict()
            if not word in TAGS[tag]:
                TAGS[tag][word] = 1
            else:
                TAGS[tag][word] = TAGS[tag][word] + 1
        #End of word in line
    # End of line in fhand
    fhand.close()

#==============================================================================
def main():
    getEmission()

#==============================================================================
if __name__ == '__main__':
    main()
#==============================================================================
