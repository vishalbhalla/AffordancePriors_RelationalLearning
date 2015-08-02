__author__ = 'vishal'


text_file = open('FilteredSVOTuples.txt', 'w')

lsGrammarTuples=[]
for line in open( 'ParsedGrammarTuples.txt', 'r' ).readlines():
    lsGrammarTuples.append( line )

    print 'Start the Filtering process to retain only nusbj and dobj SD pairs from all grammar tuples'

    for pair in lsGrammarTuples:
        if 'nsubj' in pair or 'dobj' in pair:
            text_file.write(pair)    # + "\n"

text_file.close()

print 'Filtering to retain only nusbj and dobj SD pairs from all grammar tuples is completed'

