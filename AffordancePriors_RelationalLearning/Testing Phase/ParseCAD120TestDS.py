
__author__ = 'vishal'

import os
import os.path
from nltk.stem import PorterStemmer, WordNetLemmatizer

#1204144410,stacking,subject1,1:box,2:box,3:box,4:box,
#1204144736,stacking,subject1,1:bowl,2:bowl,3:bowl,
#1204145234,stacking,subject1,1:plate,2:plate,3:plate,4:plate,5:plate,

pathTestData = '/home/vishal/Downloads/Test Data'

text_file = open('ParsedCAD120SVOTuples.txt', 'w')

labelPath = []
for dirpath, dirnames, files in os.walk(pathTestData):
    for activityfolder in dirnames:
        labelPath.append(dirpath + '/' + activityfolder)



for filePath in labelPath:
    activityFileName = filePath + '/' +  'activityLabel.txt'
    if os.path.isfile(activityFileName):

        ActivityLabel = []
        ActivityLabelList = []
        Labeling = []
        verbNounPair = ''
        noObjects = 0

        for line in open(activityFileName, 'r').readlines():
            ActivityLabel = line.rstrip('\r\n').split(',')
            # Remove empty elements from the list above
            ActivityLabel = filter(None, ActivityLabel)
            ActivityLabelList.append(ActivityLabel)


        #1204144410,1,61,null,stationary,stationary,stationary,stationary
        #1204144410,62,100,reaching,stationary,stationary,stationary,reachable
        labelingFileName = filePath + '/' +  'labeling.txt'
        for line in open(labelingFileName, 'r').readlines():
            Labeling = line.rstrip('\r\n').split(',')
            if Labeling[3] != 'null':
                for activity in ActivityLabelList:
                    if Labeling[0] in activity[0]:
                        verbS = Labeling[3]
                        nounS = activity[2]
                        verbNounSVPair = 'nsubj(' + verbS + ', ' + nounS + ')' + '\n'
                        text_file.write(verbNounSVPair)    # + "\n"
                        objCount = 1
                        totalElem = len(activity)
                        noObjects = totalElem - 3
                        while objCount <= noObjects:
                            if Labeling[objCount + 3] != 'stationary':
                                verbO = Labeling[objCount + 3]
                                nounwithIdx = activity[objCount + 2]
                                nounO = nounwithIdx.split(':')[1]
                                verbNounVOPair = 'dobj(' + verbO + ', ' + nounO + ')' + '\n'
                                text_file.write(verbNounVOPair)    # + "\n"
                            objCount = objCount + 1


text_file.close()


