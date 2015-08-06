__author__ = 'vishal'



from src.stanford_parser.parser import Parser
#from jpype.java.io import CharArrayReader
from jpype import *
import subprocess
import shutil


# Initialize reuseable variables
#pcfg_model_fname = "englishPCFG.ser.gz"
self = Parser(None)
lp = self.parser
tlp = self.package.trees.PennTreebankLanguagePack()
gsf = tlp.grammaticalStructureFactory()
parse = 'null'
tdl = 'null'
strGrammarTuples = ''
text_file = open('ParsedGrammarTuples.txt', 'w')

for sentence in open( 'WebScrapingTrain.txt', 'r' ).readlines():
    dependencies = self.parseToStanfordDependencies(sentence)
    #tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]

    #token, trees = self.parse(sentence)

    parse = lp.getBestParse()

    gs = gsf.newGrammaticalStructure(parse)
    tdl = gs.typedDependenciesCollapsed()

    #print tdl
    strGrammarTuples = str(tdl) #making data as string to avoid buffer error

    #Append to new lines
    strGrammarTuples.replace('), ', ')\n')

    strGrammarTuples = strGrammarTuples.replace('), ', ')\n')
    
    strGrammarTuples = strGrammarTuples.replace(')', ')\n')
    strGrammarTuples = strGrammarTuples.replace('\'', '')
    strGrammarTuples = strGrammarTuples.translate(None, '[]')

    text_file.write(strGrammarTuples)

    # Dispose off objects by assigning it to null.
    dependencies = 'null'
    parse = 'null'
    gs = 'null'
    tdl = 'null'
    strGrammarTuples = ''
    
text_file.close()

# End of Iteratively parsing each line into its Stanford Typed Dependencies.


# Filter out only nusbj and dobj Stanford Dependency pairs from all grammar tuples.

#inputFileName = 'ParsedGrammarTuples.txt'
#outputFileName = 'FilteredSVOTuples.txt'

execfile('FilterSVOTuples.py')

# Filter the positions numbers from each verb-noun grammar tuple.

#inputFileName = 'FilteredSVOTuples.txt'
#outputFileName = 'FormattedTuples.txt'

execfile('FilterPositions.py')

