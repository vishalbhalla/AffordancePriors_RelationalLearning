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



### Evaluation
dobjCAD120Eval = []
# Open the dobj CAD 120 file & Get Distinct dobj CAD 120 Tuples
for line in open('CAD120SVOTuples.txt', 'r').readlines():
    if 'dobj' in line: #dobj("Reach","Microwave")
        tupleEval = line.split(',')
        strObject = tupleEval[1].strip().replace('"','').replace(')','')
        if not strObject in dobjCAD120Eval:
            dobjCAD120Eval.append(strObject)

print len(dobjCAD120Eval)



# 4. For each entity in the VO - MAP file [dobj(Verb, Entity)] of CAD 120
objCorrectClasify = []
objMisClasify = []
objBothClasify = []
objOutOfVocab = []
for obj in dobjCAD120Eval: # For each distinct entity in the CAD 120 dobj(Verb, Entity)] file
     strObjExists = False
     for tupleObj in objPassivity:
         strObj = tupleObj[0]
         strPassivity = tupleObj[1]
         if strObj == obj:  # If dobj entity exists -> What is the corresponding label from Training
             if strPassivity == 'Passive': # dobj is more or dobj entity doesn't exist in nsubj -> Passive
                 objCorrectClasify.append(obj)
             elif strPassivity == 'Active': # nsubj is more -> Active
                 objMisClasify.append(obj)
             elif strPassivity == 'Both': # dobj = nsubj -> Both
                 objBothClasify.append(obj)

             # dobj entity exists in CAD 120 dobj(Verb, Entity)]
             strObjExists = True
             break

     if strObjExists == False: # dobj entity doesn't exist in dobj entity exists in CAD 120 dobj(Verb, Entity)] -> Out of Vocabulary
         objOutOfVocab.append(obj)



# 5. Draw Table with these 3 values for different number of links.
# No of links vs (Passive correct, passive misclassified and out of vocabulary)
print len(objCorrectClasify)
print len(objMisClasify)
print len(objBothClasify)
print len(objOutOfVocab)
