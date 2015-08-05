
__author__ = 'vishal'


import shutil

'''

import os
import os.path
from nltk.stem import PorterStemmer, WordNetLemmatizer


## Stemming
# Stemming is the process of reducing a word into its stem, i.e. its root form.
# We are doing the stemming for comparison of our corpuses (train & test) nd it doesnt matter if we don't get a real world.
stemmer = PorterStemmer()


## Lemmatisation
# The purpose of Lemmatisation is to group together different inflected forms of a word, called lemma.
# It maps several words into one common root.
lemmatiser = WordNetLemmatizer()

#1204144410,stacking,subject1,1:box,2:box,3:box,4:box,
#1204144736,stacking,subject1,1:bowl,2:bowl,3:bowl,
#1204145234,stacking,subject1,1:plate,2:plate,3:plate,4:plate,5:plate,

pathTestData = '/home/vishal/Downloads/Test Data'

text_file = open('ParsedCAD120SVOTuples.txt', 'w')

labelPath = []
for dirpath, dirnames, files in os.walk(pathTestData):
    for activityfolder in dirnames:
        labelPath.append(dirpath + '/' + activityfolder)



for filePath in labelPath:
    activityFileName = filePath + '/' +  'activityLabel.txt'
    if os.path.isfile(activityFileName):

        ActivityLabel = []
        ActivityLabelList = []
        Labeling = []
        verbNounPair = ''
        noObjects = 0

        for line in open(activityFileName, 'r').readlines():
            ActivityLabel = line.rstrip('\r\n').split(',')
            # Remove empty elements from the list above
            ActivityLabel = filter(None, ActivityLabel)
            ActivityLabelList.append(ActivityLabel)


        #1204144410,1,61,null,stationary,stationary,stationary,stationary
        #1204144410,62,100,reaching,stationary,stationary,stationary,reachable
        labelingFileName = filePath + '/' +  'labeling.txt'
        for line in open(labelingFileName, 'r').readlines():
            Labeling = line.rstrip('\r\n').split(',')
            if Labeling[3] != 'null':
                for activity in ActivityLabelList:
                    if Labeling[0] in activity[0]:
                        verbS = Labeling[3]
                        nounS = activity[2]

                        strVerbNewS = ''
                        if verbS.endswith('ing'):
                            strVerbNewS = verbS[:-3] + 'e'
                        if verbS.endswith('to'):
                            strVerbNewS = verbS[:-2] + 'e'
                        if verbS.endswith('able'):
                            strVerbNewS = verbS[:-4] +'e'

                        # Stem to find the root word.
                        strStemmedVerbS = stemmer.stem(strVerbNewS)
                        verbS = strStemmedVerbS

                        # Remove numbers from the Subject
                        nounS = nounS.translate(None, '-0123456789')

                        verbNounSVPair = 'nsubj(' + verbS + ', ' + nounS + ')' + '\n'

                        text_file.write(verbNounSVPair)    # + "\n"
                        objCount = 1
                        totalElem = len(activity)
                        noObjects = totalElem - 3
                        while objCount <= noObjects:
                            if Labeling[objCount + 3] != 'stationary':
                                verbO = Labeling[objCount + 3]
                                nounwithIdx = activity[objCount + 2]
                                nounO = nounwithIdx.split(':')[1]

                                strVerbNewO = ''
                                if verbO.endswith('ing'):
                                    strVerbNewO = verbO[:-3] + 'e'
                                if verbO.endswith('to'):
                                    strVerbNewO = verbO[:-2] + 'e'
                                if verbO.endswith('able'):
                                    strVerbNewO = verbO[:-4] +'e'

                                # Stem to find the root word.
                                strStemmedVerbO = stemmer.stem(strVerbNewO)
                                verbO = strStemmedVerbO

                                # Remove numbers from Object
                                nounO = nounO.translate(None, '-0123456789')

                                verbNounVOPair = 'dobj(' + verbO + ', ' + nounO + ')' + '\n'
                                text_file.write(verbNounVOPair)    # + "\n"
                            objCount = objCount + 1

text_file.close()


#text_fileLemma = open('CAD120SVOTuplesLemmatized.txt', 'w')
text_fileLemma = open('CAD120SVOTuplesStemmedLemmatized.txt', 'w')

print 'Start the Lemmatization process to group together different words (lemma) to a common root for all grammar tuples'

text_file = open('ParsedCAD120SVOTuples.txt', 'r')
VerbNounTuples = text_file.read()
text_file.close()

SVOTuples = VerbNounTuples.split('\n')
for pair in SVOTuples:
    if 'nsubj' in pair or 'dobj' in pair:
        str = pair.strip()
        if 'nsubj' in pair:
            formattedStr = str.replace('nsubj(', '')
        elif 'dobj' in pair:
            formattedStr = str.replace('dobj(', '')
        formattedStr = formattedStr.replace(')', '')
        formattedStr = formattedStr.translate(None, ' ')
        lsVerbNoun = []
        lsVerbNoun = formattedStr.split(',')
        strVerb = lsVerbNoun[0]
        strNoun = lsVerbNoun[1]

        #strStemmedVerb = stemmer.stem(strVerb)
        #strStemmedNoun = stemmer.stem(strNoun)

        strLemmatizedVerb = lemmatiser.lemmatize(strVerb, pos="v")
        strLemmatizedNoun = lemmatiser.lemmatize(strNoun, pos="n")

        if 'nsubj' in pair:
            lemmatizeSVOTuple = 'nsubj(' + strLemmatizedVerb + ',' + strLemmatizedNoun + ')'
        elif 'dobj' in pair:
            lemmatizeSVOTuple = 'dobj(' + strLemmatizedVerb + ',' + strLemmatizedNoun + ')'
        text_fileLemma.write(lemmatizeSVOTuple + "\n")

text_fileLemma.close()
print 'Lemmatization process to group together different words (lemma) to a common root for all grammar tuples is completed'

'''

text_file = open('CAD120SVOTuples.txt', 'w')

print 'Start the Formatting of verb-noun grammar tuples to be represented in the Alchemy MLN format for Relational Learning'
for line in open( 'CAD120SVOTuplesStemmedLemmatized.txt', 'r' ).readlines():
    #Capitalize first letter of each word 
    formattedStr = line.title()
    formattedStr = formattedStr.replace('Nsubj', 'nsubj')
    formattedStr = formattedStr.replace('Dobj', 'dobj')
    
    # Group Animate subjects higher up in the hierarchy for comparison.
    formattedStr = formattedStr.replace('Subject', 'Person')
    
    # Check for empty strings in Verb Noun tuple format
    SVOTuples = formattedStr.strip()
    SVOTuples = SVOTuples.replace('nsubj(', '')
    SVOTuples = SVOTuples.replace('dobj(', '')
    SVOTuples = SVOTuples.replace(')', '')
    SVOTuplesPairs = SVOTuples.split(',')
    if SVOTuplesPairs[0] and SVOTuplesPairs[1] :
        text_file.write(formattedStr)    # + "\n"

text_file.close()
print 'Formatting of verb-noun grammar tuples to be represented in the Alchemy MLN format for Relational Learning is completed'


# Copy the file for MLN Weight Learning and Inference using Alchemy.
shutil.copy('CAD120SVOTuples.txt', '../Alchemy Relational Learning/')
print 'Copied CAD120SVOTuples.txt file for MLN Weight Learning and Inference using Alchemy.'
