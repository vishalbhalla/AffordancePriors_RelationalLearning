__author__ = 'vishal'


from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen

#URLList = ["http://www.wikihow.com/Open-a-Bottle-of-Water", "http://www.wikihow.com/Install-a-Ceiling-Fan", "http://www.wikihow.com/Shut-a-Door-Quietly", "http://www.wikihow.com/Open-and-Care-for-a-Book", "http://www.wikihow.com/Move-a-Refrigerator"]
URLList = ["http://www.wikihow.com/Open-a-Bottle-of-Water", "http://www.wikihow.com/Install-a-Ceiling-Fan",
           "http://www.wikihow.com/Shut-a-Door-Quietly", "http://www.wikihow.com/Open-and-Care-for-a-Book",
           "http://www.wikihow.com/Move-a-Refrigerator", "http://www.wikihow.com/Open-a-Sealed-Envelope",
           "http://www.wikihow.com/Open-a-Stuck-Window", "http://www.wikihow.com/Dust-Your-Entire-House",
           "http://www.wikihow.com/Clean-Gold-Plated-Watches", "http://www.wikihow.com/Clean-a-Clothes-Dryer-Vent",
           "http://www.wikihow.com/Clean-Windows", "http://www.wikihow.com/Bet-on-the-World-Cup",
           "http://www.wikihow.com/Set-a-Table", "http://www.wikihow.com/Make-Spring-Roll-Wrappers",
           "http://www.wikihow.com/Choose-Microwave-Safe-Containers", "http://www.wikihow.com/Use-a-Microwave",
           "http://www.wikihow.com/Clean-a-Sponge", "http://www.wikihow.com/Make-Condensed-Milk",
           "http://www.wikihow.com/Make-Kefir", "http://www.wikihow.com/Make-Vegan-Condensed-Milk",
           "http://www.wikihow.com/Access-Another-Computer-from-Your-Computer", "http://www.wikihow.com/Repair-a-Remote-Control",
           "http://www.wikihow.com/Test-if-a-Dish-Is-Microwave-Safe", "http://www.wikihow.com/Install-a-Microwave",
           ]



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

# Handle special characters like apostrophe
#txtString = txtString.replace("\'", '')
txtString = txtString.replace('"', '')
#txtString = txtString.replace('(', '')
#txtString = txtString.replace(')', '')

text_file.write(txtString)    # + "\n"
text_file.close()
