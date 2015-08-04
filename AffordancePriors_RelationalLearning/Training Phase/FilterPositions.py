__author__ = 'vishal'

import shutil

text_file = open('FormattedTuples.txt', 'w')

print 'Start the Filtering process of positions on each verb-noun grammar tuple'
for line in open( 'FilteredSVOTuples.txt', 'r' ).readlines():
    str = line
    formattedStr = str.translate(None, '-0123456789')
    #Capitalize first letter of each word 
    formattedStr = formattedStr.title()
    formattedStr = formattedStr.replace('Nsubj', 'nsubj')
    formattedStr = formattedStr.replace('Dobj', 'dobj')

    text_file.write(formattedStr)    # + "\n"

text_file.close()
print 'Filtering of positions for each verb-noun grammar tuple is completed'


# Copy the file for MLN Weight Learning and Inference using Alchemy.
shutil.copy('FormattedTuples.txt', '../Alchemy Relational Learning/')
print 'Copied FormattedTuples.txt file for MLN Weight Learning and Inference using Alchemy.'