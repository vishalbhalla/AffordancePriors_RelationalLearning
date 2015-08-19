__author__ = 'vishal'

import math
weightedSVOTuples = []
for line in open( 'learnwts.mln', 'r' ).readlines():
    # Remove comments before every weight and verb-noun pairs in the file.
    if not '//' in line and not line.startswith('nsubj(') and not line.startswith('dobj('): #and not '' in line:
        if not '\n' == line:
            SVOTuples = line.split('  ')
            weightedSVOTuples.append((float(SVOTuples[0]),SVOTuples[1]))

# Sort based on dependencies i.e. nsubj and dobj
weightedSVOTuples.sort(key=lambda x: x[1])

# Split based on nsubj and dobj
weightedSVTuples = [x for x in weightedSVOTuples if x[1].startswith('nsubj(')]
weightedVOTuples = [x for x in weightedSVOTuples if x[1].startswith('dobj(')]

# Sort based on weights for individual verb-noun dependencies
weightedSVTuples.sort(key=lambda x: x[0])
weightedVOTuples.sort(key=lambda x: x[0])

# Filter percentage of the tuples
p = 0.4

lenSV = len(weightedSVTuples)
filteredSV = int(math.ceil(p*lenSV))
filteredSVTuples = weightedSVTuples[filteredSV:]

lenVO = len(weightedVOTuples)
filteredVO = int(math.ceil(p*lenVO))
filteredVOTuples = weightedVOTuples[filteredVO:]

# Append the Predicate declarations to the start of the file as earlier
predDecl = ''
predDecl += '//predicate declarations' + '\n'
predDecl += 'dobj(verb,object)' + '\n'
predDecl += 'nsubj(verb,subject)' + '\n'

# Append the filtered weighted tuples
strSortedWeightedTuples = ''
strSortedWeightedTuples += predDecl
strSortedWeightedTuples += ''.join([str(tup[0]) + '  ' + str(tup[1]) for tup in filteredSVTuples])
strSortedWeightedTuples += ''.join([str(tup[0]) + '  ' + str(tup[1]) for tup in filteredVOTuples])

# Write the filtered learned weights of the SVO tuples to a file
text_file = open('filterlearnwts.txt', 'w')
text_file.write(strSortedWeightedTuples)
text_file.close()
