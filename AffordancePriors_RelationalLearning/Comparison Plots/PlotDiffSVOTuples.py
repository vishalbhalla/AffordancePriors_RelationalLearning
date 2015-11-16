__author__ = 'vishal'

import numpy as np
import pylab as plt
import numpy

# text_file = open('InferenceWebScrapedSVOTuples.txt', 'r')
text_file = open('inferenceTrain.txt', 'r')
VerbNounTuplesTrain = text_file.read()
text_file.close()
SVOTuplesTrain = VerbNounTuplesTrain.split('\n')


newSVOTupleTrain = []
for pair in SVOTuplesTrain:
    tupleTrain = pair.split('\t')
    if 'nsubj' in pair or 'dobj' in tupleTrain[1]:
        str = tupleTrain[1].strip()
        formattedSVOTupleTrain = str.translate(None, ' ')
        probSVOTupleTrain = float(tupleTrain[0])
        newSVOTupleTrain.append((formattedSVOTupleTrain,probSVOTupleTrain))


'''
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
'''

# Extract only ground truth tuples from test data for comparison or evaluation

text_file = open('CAD120SVOTuples.txt', 'r')
VerbNounTuplesTest = text_file.read()
text_file.close()
SVOTuplesTest = VerbNounTuplesTest.split('\n')

# Select distinct elements
CAD120SVOTuplesTest = list(set(SVOTuplesTest))
# Remove empty strings
CAD120SVOTuplesTest = filter(None, CAD120SVOTuplesTest)

text_file = open('inferenceCAD120Test.txt', 'r')
VerbNounTuplesTrain = text_file.read()
text_file.close()
SVOTupleTestInf = VerbNounTuplesTrain.split('\n')


newSVOTupleTestInf = []
listExists = []
for pair in SVOTupleTestInf:
    TupleTestInf = pair.split('\t')
    if 'nsubj' in pair or 'dobj' in TupleTestInf[1]:
        str = TupleTestInf[1].strip()
        formattedSVOTupleTestInf = str.translate(None, ' ')
        listExists = [formattedSVOTupleTestInf in [item for item in CAD120SVOTuplesTest]]
        if listExists[0]:
            probSVOTupleTestInf = float(TupleTestInf[0])
            newSVOTupleTestInf.append((formattedSVOTupleTestInf,probSVOTupleTestInf))

# End of extracting only ground truth tuples from test data for comparison or evaluation


#newSVOTuplesTrainTest = []
newSVOTuples = []
newProbSVOTuplesTrain = []
newProbSVOTuplesTest = []

for tupleTrain in newSVOTupleTrain:
     strTupleTrain = tupleTrain[0]
     probSVOTupleTrain = tupleTrain[1]
     for tupleTest in newSVOTupleTestInf: #newSVOTupleTest: # Changed to compare only with ground truth tuples from test data.
        strTupleTest = tupleTest[0]
        probSVOTupleTest = tupleTest[1]
        if strTupleTrain == strTupleTest:
            #newSVOTuplesTrainTest.append((strTupleTrain, probSVOTupleTrain, probSVOTupleTest))
            newSVOTuples.append(strTupleTrain)
            newProbSVOTuplesTrain.append(probSVOTupleTrain)
            newProbSVOTuplesTest.append(probSVOTupleTest)


print newProbSVOTuplesTrain
print newProbSVOTuplesTest


'''
# for 6 links
newProbSVOTuplesTrain = [0.04, 0.0, 0.0, 0.12]
newProbSVOTuplesTest = [1.0, 1.0, 1.0, 1.0]
newSVOTuples = ['dobj("Place","Box")', 'dobj("Pour","Milk")', 'nsubj("Place","Person")', 'nsubj("Pour","Person")']
'''

# Calculate the probabilities relative to maximum value of the Train & Test datasets.
arrNewProbSVOTuplesTrain = numpy.array(newProbSVOTuplesTrain)
arrNewProbSVOTuplesTest = numpy.array(newProbSVOTuplesTest)

relDiffTrain = arrNewProbSVOTuplesTrain/max(arrNewProbSVOTuplesTrain)
relDiffTest = arrNewProbSVOTuplesTest/max(arrNewProbSVOTuplesTest)

'''
# Calculate the average difference between the Train & Test datasets.
arrDiffTrainTest = abs(arrNewProbSVOTuplesTrain - arrNewProbSVOTuplesTest)
avgDiff = numpy.average(arrDiffTrainTest)

relDiffTrain1 = arrDiffTrainTest/arrNewProbSVOTuplesTrain
relDiffTest1 = arrDiffTrainTest/arrNewProbSVOTuplesTest
'''

print newSVOTuples

# Plot the graph for the common tuples and their probabilities.
# Scatter Plot
SVOTupleNo = range(len(newSVOTuples))
plt.xticks(SVOTupleNo, newSVOTuples)

#train = plt.scatter(SVOTupleNo,newProbSVOTuplesTrain,color='k')
#test = plt.scatter(SVOTupleNo,newProbSVOTuplesTest,color='g')

train = plt.scatter(SVOTupleNo,relDiffTrain,color='r')
test = plt.scatter(SVOTupleNo,relDiffTest,color='b')

plt.title("Scatter Plot for Inferred SVO Tuple Probabilities of WikiHow Training Dataset vs Ground Truth of CAD 120 Test Dataset")
plt.xlabel("SVO Tuples - Verb-Noun Pairs")
plt.ylabel("Probability")
plt.legend((train, test),
           ('WikiHow Training Dataset', 'CAD 120 Test Dataset'),
           scatterpoints=1,
           loc='upper right',
           ncol=1,
           fontsize=8)
plt.show()

'''
# Histogram
totaNoBins = len(newSVOTuples)
plt.hist(newProbSVOTuplesTrain, histtype='stepfilled', stacked=True, color='k', label='Inferred WikiHow Training dataset')
plt.hist(newProbSVOTuplesTest, histtype='stepfilled', stacked=True, color='g', label='Ground truth of CAD 120 Test dataset')
plt.title("Histogram of SVO Tuple Probabilities for Inferred WikiHow Training dataset vs ground truth of CAD 120 Test dataset")
plt.xlabel("SVO Tuples - Verb-Noun Pairs")
plt.ylabel("Probability")
plt.legend()

plt.show()

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *

import numpy as np
x0 = np.random.randn(500)
x1 = np.random.randn(500)+1

trace1 = Histogram(
    x=x0,
    opacity=0.75
)
trace2 = Histogram(
    x=x1,
    opacity=0.75
)
data = Data([trace1, trace2])
layout = Layout(
    barmode='overlay'
)
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='overlaid-histogram')

'''


# Calculate the L1 and L2 norm of the difference in probabilities of the Train & Test datasets.
arrNewProbSVOTuplesTrain = numpy.array(newProbSVOTuplesTrain)
arrNewProbSVOTuplesTest = numpy.array(newProbSVOTuplesTest)

# Calculate the difference between the Train & Test datasets.
arrDiffTrainTest = abs(arrNewProbSVOTuplesTrain - arrNewProbSVOTuplesTest)

'''
l1norm = sum(arrDiffTrainTest)
l2norm = arrDiffTrainTest * numpy.transpose(arrDiffTrainTest)

print 'l1norm is  ', l1norm
print 'l2norm is  ', l2norm
'''


l1norm = numpy.linalg.norm(arrDiffTrainTest, ord=1)
l2norm = numpy.linalg.norm(arrDiffTrainTest, ord=2)

print 'l1norm is  ', l1norm
print 'l2norm is  ', l2norm


