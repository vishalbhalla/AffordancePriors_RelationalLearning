__author__ = 'vishal'


import subprocess
import shutil
# Build the vocabulary set for Subject, Verb and Object to be appended in the Alchemy Learned Weights file.

print 'Start building the vocabulary set for Subject, Verb and Object to be appended in the Alchemy Learned Weights file.'
vocabSubject=[]
vocabVerb=[]
vocabObject=[]
verbNounPair=[]
for line in open( 'FormattedTuples.txt', 'r' ).readlines():
    str = line
    if 'nsubj' in str:
        formattedStr = str.replace('nsubj(', '')
        formattedStr = formattedStr.replace(')', '')
        formattedStr = formattedStr.translate(None, ' ')
        lsSV = []
        lsSV = formattedStr.split(',')
        strVerb = lsSV[0]
        strSubject = lsSV[1]
        if strVerb not in vocabVerb:
            vocabVerb.append(strVerb)
        if strSubject not in vocabSubject:
            vocabSubject.append(strSubject)
            
    if 'dobj' in str:
        formattedStr = str.replace('dobj(', '')
        formattedStr = formattedStr.replace(')', '')
        formattedStr = formattedStr.translate(None, ' ')
        lsVO = []
        lsVO = formattedStr.split(',')
        strVerb = lsVO[0]
        strObject = lsVO[1]
        if strVerb not in vocabVerb:
            vocabVerb.append(strVerb)
        if strObject not in vocabObject:
            vocabObject.append(strObject)
            

print 'The vocabulary set for Subject, Verb and Object to be appended in the Alchemy Learned Weights file is built.'
strVocabSubject = ','.join(vocabSubject)
strVocabVerb = ','.join(vocabVerb)
strVocabObject = ','.join(vocabObject)

strVocabSubject = '{' + strVocabSubject + '}'
strVocabVerb = '{' + strVocabVerb + '}'
strVocabObject = '{' + strVocabObject + '}'

# SVO Tuple Database
dbSVO = '~/' + 'Downloads/alchemy-2/exdata/vishal-test/SVOTuples.db'
#shutil.copy2('FormattedTuples.txt', dbSVO)
    
#Build the predicate formula file

strConstantSubjects = 'subject = ' + strVocabSubject
strConstantObjects = 'object = ' + strVocabObject
strConstantVerbs = 'verb = ' + strVocabVerb
strPredicateFormulaFile = 'nsubj(verb,subject)' + '\n' + 'dobj(verb,object)' + '\n'

strPredicateFormula = '// Learn weight for each verb noun pair' + '\n' + 'nsubj(v, +s)' + '\n' + 'dobj(v, +o)' + '\n'
strPredicateFormulaFile = strPredicateFormulaFile + strPredicateFormula

#print strPredicateFormulaFile
text_file = open('SVOPredicateFormula.mln', 'w')
text_file.write(strPredicateFormulaFile)
text_file.close()

print 'SVO Predicate Formula file built.'

# Use Alchemy MLN for Weight Learning.
command = 'cd ' + '~/' + 'Downloads/alchemy-2/bin'

# Add the constants i.e. vocabulary set of subject and objects in the SVOPredicateFormula.mln file.
#command = command + '\n' + 'echo ' + strConstantSubjects + ' >> ../exdata/vishal-test/SVOPredicateFormula.mln'
#command = command + '\n' + 'echo ' + strConstantObjects + ' >> ../exdata/vishal-test/SVOPredicateFormula.mln'
#command = command + '\n' + 'echo ' + strConstantVerbs + ' >> ../exdata/vishal-test/SVOPredicateFormula.mln'

#command = command + '\n' + './learnwts -i ../exdata/vishal-test/SVOPredicateFormula.mln -o ../exdata/vishal-test/learnwts.mln -t ../exdata/vishal-test/empty.db -ne nsubj, dobj -noAddUnitClauses'
#command = command + '\n' + './learnwts -i ../exdata/vishal-test/SVOPredicateFormula.mln -o ../exdata/vishal-test/learnwts.mln -t ../exdata/vishal-test/SVOTuples.db -ne nsubj, dobj -noAddUnitClauses'
command = command + '\n' + './learnwts -g -i ../exdata/vishal-test/SVOPredicateFormula.mln -o ../exdata/vishal-test/learnwts.mln -t ../exdata/vishal-test/SVOTuples.db -noAddUnitClauses'

# Add the constants i.e. vocabulary set for verbs in the learnwts.mln file.
command = command + '\n' + 'echo ' + strConstantVerbs + ' >> ../exdata/vishal-test/learnwts.mln'

# Use Alchemy MLN for Inference.
#command = command + '\n' + './infer -i ../exdata/vishal-test/learnwts.mln -r ../exdata/vishal-test/inference.mln -e ../exdata/vishal-test/empty.db -q nsubj, dobj'
command = command + '\n' + './infer -p -i ../exdata/vishal-test/learnwts.mln -r ../exdata/vishal-test/inference.mln -e ../exdata/vishal-test/empty.db -q nsubj,dobj'

text_file = open('executeAlchemyMLN.sh', 'w')
text_file.write(command)
text_file.close()

print 'executeAlchemyMLN script file built.'
#subprocess.call('chmod +x executeAlchemyMLNWeightLearning.sh')
subprocess.Popen(['./executeAlchemyMLN.sh'], shell=True)
