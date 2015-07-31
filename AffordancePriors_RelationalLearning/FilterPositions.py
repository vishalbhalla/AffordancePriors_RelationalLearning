__author__ = 'vishal'

class FilterPositions(object):

    def filterPositions(self, inputFileName, outputFileName):
        verbNounPair=[]
        for line in open( 'FilteredSVOTuples.txt', 'r' ).readlines():
            verbNounPair.append( line )

        print 'Start the Filtering process of positions on each verb-noun grammar tuple'

        text_file = open('FormattedTuples.txt', 'w')

        for pair in verbNounPair:
            str = pair
            formattedStr = str.translate(None, '-0123456789')
            text_file.write(formattedStr)    # + "\n"

        text_file.close()

        print 'Filtering of positions for each verb-noun grammar tuple is completed'
