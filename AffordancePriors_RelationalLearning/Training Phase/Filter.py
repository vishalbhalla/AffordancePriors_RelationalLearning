__author__ = 'vishal'

import FilterSVOTuples, FilterPositions

#import AffordancePriors_RelationalLearning
# Filter out only nusbj and dobj Stanford Dependency pairs from all grammar tuples.

#inputFileName = 'ParsedGrammarTuples.txt'
#outputFileName = 'FilteredSVOTuples.txt'

execfile('FilterSVOTuples.py')

# Filter the positions numbers from each verb-noun grammar tuple.

#inputFileName = 'FilteredSVOTuples.txt'
#outputFileName = 'FormattedTuples.txt'

execfile('FilterPositions.py')





