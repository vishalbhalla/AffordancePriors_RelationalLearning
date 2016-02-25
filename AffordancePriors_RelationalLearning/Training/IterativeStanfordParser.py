__author__ = 'vishal'


# import sys
# sys.path.append('/home/vishal/Statistical Relational Learning/AffordanceMining/AffordancePriors_RelationalLearning/AffordancePriors_RelationalLearning/Training Phase/')
# print sys.path

# import os
# print os.getcwd()
# os.path.join(os.getcwd(),'src.stanford_parser.parser')
# from parser import Parser

# try:
#     from src.stanford_parser.parser import Parser
# except ImportError:
#     print 'Import Error'
#      # from .. import src.stanford_parser.parser.Parser


# from src.stanford_parser.parser import Parser
# # from jpype import *

#
#
# import nltk.tag.stanford
# from nltk.parse.stanford import StanfordParser
#
# stanford_parser_dir = '/home/vishal/Softwares/Stanford/stanford-parser-full-2015-04-20/'
# # eng_model_path = stanford_parser_dir  + "edu/stanford/nlp/models/lexparser/englishRNN.ser.gz"
# eng_model_path = stanford_parser_dir  + "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"
# my_path_to_models_jar = stanford_parser_dir  + "stanford-parser-3.5.2-models.jar"
# my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"
#
# parser = StanfordParser(model_path=eng_model_path, path_to_models_jar=my_path_to_models_jar, path_to_jar=my_path_to_jar)
# [list(parse.triples()) for parse in parser.raw_parse("The quick brown fox jumps over the lazy dog.")]
#


# from nltk.parse.stanford import StanfordNeuralDependencyParser

from nltk.parse.stanford import StanfordDependencyParser
# dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
# dep_parser=StanfordDependencyParser(model_path='/home/vishal/Statistical Relational Learning/AffordanceMining/AffordancePriors_RelationalLearning/AffordancePriors_RelationalLearning/3rdParty/stanford-parser/stanford-parser-2010-08-25/englishPCFG.ser.gz')

# dep_parser=StanfordDependencyParser(model_path="/home/vishal/Softwares/Stanford/stanford-parser-full-2015-04-20/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

# dep_parser=StanfordDependencyParser()

# dep_parser=StanfordNeuralDependencyParser(model_path='/home/vishal/Statistical Relational Learning/AffordanceMining/AffordancePriors_RelationalLearning/AffordancePriors_RelationalLearning/3rdParty/stanford-parser/stanford-parser-2010-08-25/englishPCFG.ser.gz')

# [list(parse.triples()) for parse in dep_parser.raw_parse("The quick brown fox jumps over the lazy dog.")]


from src.stanford_parser.parser import Parser
#from jpype.java.io import CharArrayReader
from jpype import *
import subprocess
import shutil


# Initialize reuseable variables
# pcfg_model_fname = "/home/vishal/Statistical\ Relational\ Learning/Affordance Mining/AffordancePriors_RelationalLearning/AffordancePriors_RelationalLearning/3rdParty/stanford-parser/stanford-parser-2010-08-20/englishPCFG.ser.gz"
# self = Parser(pcfg_model_fname)


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

    try:
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

    except: # catch *all* exceptions
        #  Parse the next sentence.
        x = 5

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

