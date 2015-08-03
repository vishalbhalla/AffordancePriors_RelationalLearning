__author__ = 'vishal'


from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen

URLList = ["http://www.wikihow.com/Use-Citrus-Fruit-Peels-in-the-Home-and-Garden", "http://www.wikihow.com/Place-and-Finish-a-Concrete-Floor"]
txtString = ''
text_file = open('WebScrapingTrainSentence.txt', 'w')

for BASE_URL in URLList:
    html = urlopen(BASE_URL).read()
    soup = BeautifulSoup(html, "lxml")
    sectionDiv = soup.findAll("div","step")
    for item in sectionDiv:
        listTags = item.findAll('li')
        for childTag in listTags:
            for grandchildTag in childTag:
                if type(grandchildTag.string) == NavigableString:
                    txtString += grandchildTag.string.encode('ascii', 'ignore').encode('utf-8')
    txtString += "\n"+ "\n"+ "\n"

text_file.write(txtString)    # + "\n"
text_file.close()
