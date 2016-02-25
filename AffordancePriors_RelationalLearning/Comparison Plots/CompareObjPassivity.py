__author__ = 'vishal'

import numpy as np
#import pylab as plt
import os


# Open the nsubj Inference file
text_file = open('outSV.txt')
VerbNounTuplesTrain = text_file.read()
text_file.close()
SVTuplesTrain = VerbNounTuplesTrain.split('\n')


# 0.4885	nsubj("verb", "You")
nsubjTrain = []
for pair in SVTuplesTrain:
    tupleTrain = pair.split('\t')
    strTuple = tupleTrain[1].strip().split(',')
    strSubject = strTuple[1].strip().replace('"','').replace(')','')
    probSVTupleTrain = float(tupleTrain[0])
    nsubjTrain.append((strSubject,probSVTupleTrain))

print len(nsubjTrain)
print nsubjTrain[1]



# Open the dobj Inference file
text_file = open('outVO.txt')
VerbNounTuplesTrain = text_file.read()
text_file.close()
VOTuplesTrain = VerbNounTuplesTrain.split('\n')


# 0.2305	dobj("verb", "Milk")
dobjTrain = []
for pair in VOTuplesTrain:
    tupleTrain = pair.split('\t')
    strTuple = tupleTrain[1].strip().split(',')
    strObject = strTuple[1].strip().replace('"','').replace(')','')
    probVOTupleTrain = float(tupleTrain[0])
    dobjTrain.append((strObject,probVOTupleTrain))


print len(dobjTrain)
print dobjTrain[1]

# 3. Compare the (ve, Entity) tuple in train SV and VO - MAP file to decide whether it is active or passive

objPassivity = []
for tupleObj in dobjTrain: # For each entity in the VO - MAP file [dobj(Verb, Entity)]
     strObj = tupleObj[0]
     probVOTuple = tupleObj[1]
     strObjExists = False
     for tupleSubj in nsubjTrain:
        strSubj = tupleSubj[0]
        probSVTuple = tupleSubj[1]
        if strObj == strSubj:
            if probVOTuple > probSVTuple: # dobj is more -> Passive
                objPassivity.append((strObj,'Passive'))
            elif probVOTuple < probSVTuple: # nsubj is more -> Active
                objPassivity.append((strObj,'Active'))# Active
            elif probVOTuple == probSVTuple: # dobj = nsubj -> Both
                objPassivity.append((strObj,'Both'))

            # dobj entity exists in nsubj
            strObjExists = True
            break

     if strObjExists == False: # dobj entity doesn't exist in nsubj -> Passive
         objPassivity.append((strObj,'Passive'))



print len(objPassivity)

