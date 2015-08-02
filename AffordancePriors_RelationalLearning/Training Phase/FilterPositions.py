__author__ = 'vishal'


text_file = open('FormattedTuples.txt', 'w')

verbNounPair=[]
for line in open( 'FilteredSVOTuples.txt', 'r' ).readlines():
    verbNounPair.append( line )

    print 'Start the Filtering process of positions on each verb-noun grammar tuple'

    for pair in verbNounPair:
        str = pair
        formattedStr = str.translate(None, '-0123456789')
        text_file.write(formattedStr)    # + "\n"

text_file.close()

print 'Filtering of positions for each verb-noun grammar tuple is completed'
