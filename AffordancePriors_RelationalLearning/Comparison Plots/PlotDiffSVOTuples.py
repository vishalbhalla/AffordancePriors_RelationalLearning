__author__ = 'vishal'

import numpy as np
import pylab as plt

text_file = open('InferenceWebScrapedSVOTuples.txt', 'r')
VerbNounTuplesTrain = text_file.read()
text_file.close()
SVOTuplesTrain = VerbNounTuplesTrain.split('\n')


newSVOTupleTrain = []
for pair in SVOTuplesTrain:
    tupleTrain = pair.split(' ')
    if 'nsubj' in pair or 'dobj' in tupleTrain[0]:
        str = tupleTrain[0].strip()
        formattedSVOTupleTrain = str.translate(None, ' ')
        probSVOTupleTrain = float(tupleTrain[1])
        newSVOTupleTrain.append((formattedSVOTupleTrain,probSVOTupleTrain))



text_file = open('InferenceCAD120SVOTuples.txt', 'r')
VerbNounTuplesTest = text_file.read()
text_file.close()
SVOTuplesTest = VerbNounTuplesTest.split('\n')

newSVOTupleTest = []
for pair in SVOTuplesTest:
    tupleTest = pair.split(' ')
    if 'nsubj' in pair or 'dobj' in tupleTest[0]:
        str = tupleTest[0].strip()
        formattedSVOTupleTest = str.translate(None, ' ')
        probSVOTupleTest = float(tupleTest[1])
        newSVOTupleTest.append((formattedSVOTupleTest,probSVOTupleTest))


#newSVOTuplesTrainTest = []
newSVOTuples = []
newProbSVOTuplesTrain = []
newProbSVOTuplesTest = []

for tupleTrain in newSVOTupleTrain:
     strTupleTrain = tupleTrain[0]
     probSVOTupleTrain = tupleTrain[1]
     for tupleTest in newSVOTupleTest:
        strTupleTest = tupleTest[0]
        probSVOTupleTest = tupleTest[1]
        if strTupleTrain == strTupleTest:
            #newSVOTuplesTrainTest.append((strTupleTrain, probSVOTupleTrain, probSVOTupleTest))
            newSVOTuples.append(strTupleTrain)
            newProbSVOTuplesTrain.append(probSVOTupleTrain)
            newProbSVOTuplesTest.append(probSVOTupleTest)


# Plot the graph for the common tuples and their probabilities.
SVOTupleNo = range(len(newSVOTuples))
plt.xticks(SVOTupleNo, newSVOTuples)
plt.scatter(SVOTupleNo,newProbSVOTuplesTrain,color='k')
plt.scatter(SVOTupleNo,newProbSVOTuplesTest,color='g')
plt.show()
