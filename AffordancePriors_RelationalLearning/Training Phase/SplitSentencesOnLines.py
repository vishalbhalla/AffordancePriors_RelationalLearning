__author__ = 'vishal'

text_file = open('WebScrapingTrain.txt', 'w')

for sentence in open('WebScrapingTrainSentence.txt', 'r').readlines():
    newSentences = sentence.replace('.', '.\n')
    text_file.write(newSentences)

text_file.close()
