__author__ = 'vishal'


text_file = open('CAD120SVOTuples.txt', 'r')
VerbNounTuplesTest = text_file.read()
text_file.close()
SVOTuplesTest = VerbNounTuplesTest.split('\n')

# Select distinct elements
CAD120SVOTuplesTest = list(set(SVOTuplesTest))
# Remove empty strings
CAD120SVOTuplesTest = filter(None, CAD120SVOTuplesTest)

text_file = open('InferenceCAD120SVOTuples.txt', 'r')
VerbNounTuplesTrain = text_file.read()
text_file.close()
SVOTupleTestInf = VerbNounTuplesTrain.split('\n')


newSVOTupleTestInf = []
listExists = []
for pair in SVOTupleTestInf:
    TupleTestInf = pair.split(' ')
    if 'nsubj' in pair or 'dobj' in TupleTestInf[0]:
        str = TupleTestInf[0].strip()
        formattedSVOTupleTestInf = str.translate(None, ' ')
        listExists = [formattedSVOTupleTestInf in [item for item in CAD120SVOTuplesTest]]
        if listExists[0]:
            probSVOTupleTestInf = float(TupleTestInf[1])
            newSVOTupleTestInf.append((formattedSVOTupleTestInf,probSVOTupleTestInf))


# Count should be same
c = len(CAD120SVOTuplesTest)
# ct = len(newSVOTupleTestInf)
print CAD120SVOTuplesTest
