__author__ = 'vishal'

class FilterSVOTuples(object):

    def filterSVOTuples(self, inputFileName, outputFileName):

        lsGrammarTuples=[]
        for line in open( 'ParsedGrammarTuples.txt', 'r' ).readlines():
            lsGrammarTuples.append( line )

            print 'Start the Filtering process to retain only nusbj and dobj SD pairs from all grammar tuples'

            text_file = open('FilteredSVOTuples.txt', 'w')

            for pair in lsGrammarTuples:
                if 'nsubj' in pair or 'dobj' in pair:
                    text_file.write(pair)    # + "\n"

            text_file.close()

        print 'Filtering to retain only nusbj and dobj SD pairs from all grammar tuples is completed'

