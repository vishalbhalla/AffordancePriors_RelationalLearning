__author__ = 'vishal'


# Initialize reuseable variables
pcfg_model_fname = "englishPCFG.ser.gz"
self = Parser(None)
lp = self.parser
tlp = self.package.trees.PennTreebankLanguagePack()
text_file = open('ParsedGrammarTuples.txt', 'w')

for sentence in open( 'WebScrapingTrain.txt', 'r' ).readlines():
    dependencies = self.parseToStanfordDependencies(sentence)
    tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]

    token, trees = self.parse(sentence)

    parse = lp.getBestParse()

    gsf = tlp.grammaticalStructureFactory()
    gs = gsf.newGrammaticalStructure(parse)
    tdl = gs.typedDependenciesCollapsed()

    print tdl
    lsGrammarTuples=[]
    strGrammarTuples = str(tdl) #making data as string to avoid buffer error

    #Append to new lines
    strGrammarTuples.replace('), ', ')\n')

    strGrammarTuples = strGrammarTuples.replace('), ', ')\n')
    strGrammarTuples = strGrammarTuples.translate(None, '[]')

    text_file.write(strGrammarTuples)

text_file.close()


print 'Start the Filtering process to retain only nusbj and dobj SD pairs from all grammar tuples'
lsGrammarTuples=[]
for line in open( 'ParsedGrammarTuples.txt', 'r' ).readlines():
    lsGrammarTuples.append( line )
    text_file = open('FilteredSVOTuples.txt', 'w')

    for pair in lsGrammarTuples:
        if 'nsubj(' in pair or 'dobj(' in pair:
            text_file.write(pair)    # + "\n"

    text_file.close()
print 'Filtering to retain only nusbj and dobj SD pairs from all grammar tuples is completed'

