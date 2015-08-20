__author__ = 'vishal'

import shutil

text_file = open('FormattedTuples.txt', 'w')

print 'Start the Filtering process of positions on each verb-noun grammar tuple'
for line in open( 'FilteredSVOTuples.txt', 'r' ).readlines():

    # Remove position numbers from tuples
    str = line.translate(None, '-0123456789')

    # Remove special characters
    str = str.translate(None, '=*/\~+-$%.!@#^')

    # Check for empty nouns from dependency tuples or verb-noun pairs.
    if not ', )' in str and not '(,' in str:

        #Capitalize first letter of each word
        formattedStr = str.title()
        formattedStr = formattedStr.replace('Nsubj', 'nsubj')
        formattedStr = formattedStr.replace('Dobj', 'dobj')
    
        #Group Animate subjects higher up in the hierarchy for comparison.
        formattedStr = formattedStr.replace('I)', 'Person)')
        formattedStr = formattedStr.replace('You)', 'Person)')
        formattedStr = formattedStr.replace('He)', 'Person)')
        formattedStr = formattedStr.replace('She)', 'Person)')
        formattedStr = formattedStr.replace('Man)', 'Person)')
        formattedStr = formattedStr.replace('Woman)', 'Person)')
        formattedStr = formattedStr.replace('Men)', 'Person)')
        formattedStr = formattedStr.replace('Women)', 'Person)')
        formattedStr = formattedStr.replace('Child)', 'Person)')
        formattedStr = formattedStr.replace('Children)', 'Person)')
        formattedStr = formattedStr.replace('They)', 'Person)')

        text_file.write(formattedStr)    # + "\n"

text_file.close()
print 'Filtering of positions for each verb-noun grammar tuple is completed'


# Copy the file for MLN Weight Learning and Inference using Alchemy.
shutil.copy('FormattedTuples.txt', '../Alchemy Relational Learning/')
print 'Copied FormattedTuples.txt file for MLN Weight Learning and Inference using Alchemy.'