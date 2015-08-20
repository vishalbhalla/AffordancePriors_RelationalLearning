__author__ = 'vishal'

SVTuples = []
VOTuples = []
for line in open( 'SVOTuples.db', 'r' ).readlines():
    # Remove the tuple if the word Exist occurs in any of the verb-noun pairs in the file.
    if not 'Exist' in line:
        # Read verb-noun pairs in the file.
        if line.startswith('nsubj('):
            SVTuples.append(line)
        elif line.startswith('dobj('):
            VOTuples.append(line)

# Write the filtered verb-noun individual type tuples from the SVO tuples to a file
text_file = open('SVTuples.db', 'w')
strSVtuples = ''.join([str(tup) for tup in SVTuples])
text_file.write(strSVtuples)
text_file.close()

text_file = open('VOTuples.db', 'w')
strVOtuples = ''.join([str(tup) for tup in VOTuples])
text_file.write(strVOtuples)
text_file.close()
