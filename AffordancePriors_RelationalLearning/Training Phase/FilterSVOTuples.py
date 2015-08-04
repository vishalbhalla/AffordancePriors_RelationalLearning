__author__ = 'vishal'


text_file = open('FilteredSVOTuples.txt', 'w')
print 'Start the Filtering process to retain only nusbj and dobj SD pairs from all grammar tuples'

for line in open( 'ParsedGrammarTuples.txt', 'r' ).readlines():
    if line.startswith('nsubj(') or line.startswith('dobj('):
        if not '*' in line and not '%' in line and not '\'' in line:
            text_file.write(line)    # + "\n"

text_file.close()
print 'Filtering to retain only nusbj and dobj SD pairs from all grammar tuples is completed'

