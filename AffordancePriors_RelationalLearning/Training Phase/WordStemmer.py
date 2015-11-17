__author__ = 'vishal'

## Stemming
# Stemming is the process of reducing a word into its stem, i.e. its root form.
# We are doing the stemming for comparison of our corpuses (train & test) nd it doesnt matter if we don't get a real world.

## Lemmatisation
# The purpose of Lemmatisation is to group together different inflected forms of a word, called lemma.
# It maps several words into one common root.

from nltk.stem import PorterStemmer, WordNetLemmatizer

stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()

'''
strLemmatizedVerb = lemmatiser.lemmatize("Contains", pos="v")
strLemmatizedNoun = lemmatiser.lemmatize("Preventing", pos="v")

strStemmedVerbS = stemmer.stem("Contains")
strStemmedVerbO = stemmer.stem("Preventing")


strLemmatizedVerb1 = lemmatiser.lemmatize("Going", pos="v")
strLemmatizedVerb2 = lemmatiser.lemmatize("Gone", pos="v")
strLemmatizedNoun1 = lemmatiser.lemmatize("Went", pos="v")
strLemmatizedNoun2 = lemmatiser.lemmatize("Goes", pos="v")

strStemmedVerbS1 = stemmer.stem("Going")
strStemmedVerbS2 = stemmer.stem("Gone")
strStemmedVerbO1 = stemmer.stem("Went")
strStemmedVerbO2 = stemmer.stem("Goes")
'''

text_fileLemma = open('SVOTuplesLemmatized.txt', 'w')

print 'Start the Lemmatization process to group together different words (lemma) to a common root for all grammar tuples'

text_file = open('FormattedTuples.txt', 'r')
VerbNounTuples = text_file.read()
text_file.close()

SVOTuples = VerbNounTuples.split('\n')
for pair in SVOTuples:
    if 'nsubj' in pair or 'dobj' in pair:
        str = pair.strip()
        if 'nsubj' in pair:
            formattedStr = str.replace('nsubj(', '')
        elif 'dobj' in pair:
            formattedStr = str.replace('dobj(', '')
        formattedStr = formattedStr.replace(')', '')
        formattedStr = formattedStr.translate(None, ' ')
        lsVerbNoun = []
        lsVerbNoun = formattedStr.split(',')
        strVerb = lsVerbNoun[0]
        strNoun = lsVerbNoun[1]
        strLemmatizedVerb = lemmatiser.lemmatize(strVerb, pos="v")
        strLemmatizedNoun = lemmatiser.lemmatize(strNoun, pos="n")

        if 'nsubj' in pair:
            lemmatizeSVOTuple = 'nsubj(' + strLemmatizedVerb + ',' + strLemmatizedNoun + ')'
        elif 'dobj' in pair:
            lemmatizeSVOTuple = 'dobj(' + strLemmatizedVerb + ',' + strLemmatizedNoun + ')'
        text_fileLemma.write(lemmatizeSVOTuple + "\n")

text_fileLemma.close()
print 'Lemmatization process to group together different words (lemma) to a common root for all grammar tuples is completed'
