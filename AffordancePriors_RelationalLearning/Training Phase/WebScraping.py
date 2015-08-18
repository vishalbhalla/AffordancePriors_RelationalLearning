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
           'http://www.wikihow.com/Build-a-Torsion-Box-Workbench-Top','http://www.wikihow.com/Make-Popcorn-Boxes', # dobj(Reach,Box)
           'http://www.wikihow.com/Clean-a-Toilet','http://www.wikihow.com/Clean-a-Betta-Fish-Bowl','http://www.wikihow.com/Fix-an-Overflowed-Toilet-Stuffed-by-Toilet-Paper','http://www.wikihow.com/Clean-a-Toilet-With-Coke','http://www.wikihow.com/Load-a-Dishwasher','http://www.wikihow.com/Change-Your-Betta-Fish-Water','http://www.wikihow.com/Be-a-Good-Fast-Bowler', # dobj(Reach,Bowl)
           'http://www.wikihow.com/Prepare-Cereal','http://www.wikihow.com/Clean-a-Fish-Bowl','http://www.wikihow.com/Eat-a-Bowl-of-Cereal','http://www.wikihow.com/Make-Vodka-Gummy-Bear-Popsicles','http://www.wikihow.com/Unclog-a-Toilet','http://www.wikihow.com/Fix-a-Slow-Toilet', # dobj(Pour,Bowl)
           'http://www.wikihow.com/Clean-a-Microwave-With-a-Lemon','http://www.wikihow.com/Get-Bad-Smells-out-of-a-Microwave','http://www.wikihow.com/Get-Rid-of-Microwave-Smells','http://www.wikihow.com/Clean-Your-Microwave-with-Lemon-and-Vinegar','http://www.wikihow.com/Clean-a-Microwave', # dobj(Clean,Microwave)
           'http://www.wikihow.com/Organize-a-Bookshelf','http://www.wikihow.com/Read-a-Book','http://www.wikihow.com/Rebind-a-Book', #dobj(Place,Book)
           'http://www.wikihow.com/Use-the-Wii-Controller','http://www.wikihow.com/Play-Games-Well', 'http://www.wikihow.com/Bowl-an-Easy-Bowling-Strike-in-Wii-Sports', # dobj(Move,Remote)
           'http://www.wikihow.com/Microwave-Pizza-Without-the-Crust-Going-Soggy','http://www.wikihow.com/Make-an-Easter-Egg-Glow','http://www.wikihow.com/Fry-Bacon','http://www.wikihow.com/Make-a-Dinosaur-Serving-Tray','http://www.wikihow.com/Make-a-Cake-Using-a-Pressure-Cooker','http://www.wikihow.com/Blow-Bubbles','http://www.wikihow.com/Make-a-Monkey-Mask','http://www.wikihow.com/Dewax-Lemons','http://www.wikihow.com/Serve-at-a-Dinner-Party','http://www.wikihow.com/Set-a-Table', #dobj(Place,Plate)
           'http://www.wikihow.com/Clean-a-House','http://www.wikihow.com/Clean-a-Bathroom','http://www.wikihow.com/Maintain-a-Clean-Home','http://www.wikihow.com/Clean-Your-Room','http://www.wikihow.com/Keep-Your-Room-Clean','http://www.wikihow.com/Clean-a-Living-Room','http://www.wikihow.com/Clean-a-Kitchen','http://www.wikihow.com/Clean-Your-Room-Fast', # nsubj(Clean,Person)
           'http://www.wikihow.com/Play-PangYa','http://www.wikihow.com/Detect-a-Liar', # dobj(Reach,Cup)
           'http://www.wikihow.com/Litter-Train-a-Dog','http://www.wikihow.com/Build-a-Wood-Duck-House','http://www.wikihow.com/Make-a-Gift-Box','http://www.wikihow.com/Make-a-Magic-Box','http://www.wikihow.com/Measure-a-Box','http://www.wikihow.com/Catch-a-Lizard','http://www.wikihow.com/Flatten-a-Box','http://www.wikihow.com/Wrap-a-Gift-Expertly', # dobj(Place,Box)
           'http://www.wikihow.com/Use-Good-Table-Manners','http://www.wikihow.com/Throw-Wiffle-Ball-Pitches','http://www.wikihow.com/Have-Good-Manners','http://www.wikihow.com/Make-a-Hologram', # dobj(Reach,Plate)
           'http://www.wikihow.com/Set-Up-a-Hookah','http://www.wikihow.com/Clean-a-Bowl-or-Chillum','http://www.wikihow.com/Make-Distilled-Water','http://www.wikihow.com/Melt-Chocolate','http://www.wikihow.com/Make-a-Bowl-in-Minecraft','http://www.wikihow.com/Remove-a-Plate-Stuck-Inside-a-Glass-Bowl','http://www.wikihow.com/Cook-Rice','http://www.wikihow.com/Activate-Fresh-Yeast','http://www.wikihow.com/Temper-Chocolate', # dobj(Place,Bowl)
           'http://www.wikihow.com/Delete-an-eBay-Account','http://www.wikihow.com/Clear-Cookies-in-Firefox','http://www.wikihow.com/Shut-a-Door-Quietly','http://www.wikihow.com/Deal-With-the-Pain-of-a-Door-Being-Shut-on-Your-Finger','http://www.wikihow.com/Swim-Faster','http://www.wikihow.com/Close-a-Bank-Account', # nsubj(Close,Person)'
           'http://www.wikihow.com/Pack-Clothes-for-Moving','http://www.wikihow.com/Wash-Clothes-by-Hand','http://www.wikihow.com/Do-a-Simple-Coin-Magic-Trick','http://www.wikihow.com/Clean-a-Game-Disc','http://www.wikihow.com/Clean-Brass-Jewelry','http://www.wikihow.com/Make-a-Kitten-Poop','http://www.wikihow.com/Wash-Your-Clothes', # dobj(Move,Cloth)
           'http://www.wikihow.com/Open-a-Bank-Account','http://www.wikihow.com/Open-a-Pomegranate','http://www.wikihow.com/Open-Your-Locker','http://www.wikihow.com/Give-Your-Kitchen-a-Spring-Clean','http://www.wikihow.com/Organize-Kitchen-Cabinets','http://www.wikihow.com/Use-a-Smoker','http://www.wikihow.com/Eat-Durian','http://www.wikihow.com/Cook-for-Just-Yourself','http://www.wikihow.com/Use-a-Charcoal-Smoker','http://www.wikihow.com/Bake','http://www.wikihow.com/Cook-with-Just-a-Kettle','http://www.wikihow.com/Reduce-Energy-Use-While-Cooking','http://www.wikihow.com/Smoke-a-Brisket','http://www.wikihow.com/Can-Meat', # nsubj(Open,Person)
           'http://www.wikihow.com/Stop-Bottle-Feeding-Toddlers','http://www.wikihow.com/Sample/King\'s-Cup-Terms','http://www.wikihow.com/Take-Communion-in-the-Catholic-Church','http://www.wikihow.com/Cool-a-Hot-Drink-Quickly', # dobj(Drink,Cup)
           'http://www.wikihow.com/Check-a-Microwave-for-Leaks','http://www.wikihow.com/Poach-an-Egg-Using-a-Microwave','http://www.wikihow.com/Melt-Cheese-Sticks','http://www.wikihow.com/Make-Ramen-Noodles-in-the-Microwave','http://www.wikihow.com/Microwave-a-CD', # dobj(Close,Microwave)
           'http://www.wikihow.com/Lose-Weight','http://www.wikihow.com/Serve-and-Drink-Sake','http://www.wikihow.com/Make-Green-Tea','http://www.wikihow.com/Drink-Responsibly','http://www.wikihow.com/Drink-Tea-to-Lose-Weight','http://www.wikihow.com/Love-the-Taste-of-Water','http://www.wikihow.com/Make-Cabbage-Juice','http://www.wikihow.com/Make-Alcohol-from-Common-Table-Sugar','http://www.wikihow.com/Drink-More-Water-Every-Day', # nsubj(Drink,Person)
           'http://www.wikihow.com/Do-the-Cup-Song','http://www.wikihow.com/Make-a-Coffee-Cup-Using-Blender','http://www.wikihow.com/Do-the-Cup-Song-Without-a-Cup', # dobj(Move,Cup)
           'http://www.wikihow.com/Make-Coffee-without-a-Coffee-Maker','http://www.wikihow.com/Make-Cake-in-a-Mug','http://www.wikihow.com/Microwave-a-Peep','http://www.wikihow.com/Make-a-Cup-of-Tea-Using-the-Microwave','http://www.wikihow.com/Cook-Bacon-in-the-Microwave','http://www.wikihow.com/Replace-a-Microwave-Lightbulb','http://www.wikihow.com/Easily-Get-the-Stink-out-of-Your-Microwave','http://www.wikihow.com/Avoid-Making-Your-Microwave-Catch-on-Fire','http://www.wikihow.com/Microwave-Pizza-Rolls','http://www.wikihow.com/Destroy-a-Hard-Drive', # dobj(Open,Microwave)
           'http://www.wikihow.com/Move-an-Upright-Piano','http://www.wikihow.com/Arrange-Your-Furniture','http://www.wikihow.com/Move-a-Piano','http://www.wikihow.com/Convert-Within-Metric-Measurements','http://www.wikihow.com/Calculate-Chess-Tactics','http://www.wikihow.com/Use-SketchUp','http://www.wikihow.com/Decorate-a-Kitchen','http://www.wikihow.com/Make-Shawarma', # nsubj(Move,Person)
           'http://www.wikihow.com/Catalogue-Your-Books-with-Goodreads','http://www.wikihow.com/Update-Your-Page-Reading-Status-on-Goodreads','http://www.wikihow.com/Remove-a-Collection-from-a-Kindle-2','http://www.wikihow.com/Tell-if-You-Need-Glasses','http://www.wikihow.com/Build-Your-Own-Book-Truck', # dobj(Move,Book) 
           'http://www.wikihow.com/Buy-Milk','http://www.wikihow.com/Find-a-Friendly-Kitty','http://www.wikihow.com/Make-a-Thick-Strawberry-Banana-Smoothie','http://www.wikihow.com/Store-Milk',
           'http://www.wikihow.com/Pour-Beer','http://www.wikihow.com/Drink-Beer','http://www.wikihow.com/Pour-a-Drink','http://www.wikihow.com/Pour-a-Glass-of-Champagne','http://www.wikihow.com/Take-a-Bath','http://www.wikihow.com/Flambe','http://www.wikihow.com/Give-a-Kitten-a-Bath','http://www.wikihow.com/Dispose-of-Cooking-Oil','http://www.wikihow.com/Drink-Port','http://www.wikihow.com/Make-Your-Own-Bubble-Bath','http://www.wikihow.com/Make-Waffles','http://www.wikihow.com/Make-Marshmallows','http://www.wikihow.com/Make-a-Thermos','http://www.wikihow.com/Curdle-Milk','http://www.wikihow.com/Make-Chocolate-Fudge', #nsubj(Pour,Person)
           'http://www.wikihow.com/Make-Latte-Art','http://www.wikihow.com/Pasteurize-Milk', # dobj(Move,Milk)
           'http://www.wikihow.com/Install-a-Toilet','http://www.wikihow.com/Keep-Ants-Away-From-Cat-Food','http://www.wikihow.com/Make-a-Glass-Bowl-with-a-Napkin-in-Blender','http://www.wikihow.com/Play-the-Guy-Fawkes-Prank','http://www.wikihow.com/Make-a-Pot-of-Lavender-Potpourri', # dobj(Move,Bowl)
           'http://www.wikihow.com/Make-Banana-Milk','http://www.wikihow.com/Boil-Milk','http://www.wikihow.com/Froth-Milk-for-Cappuccino-Without-Fancy-Tools','http://www.wikihow.com/Make-Cardamom-Milk','http://www.wikihow.com/Make-Fruit-Custard','http://www.wikihow.com/Make-Your-Hair-Smooth-and-Shiny-with-Milk-and-Eggs','http://www.wikihow.com/Make-a-Sweet-Honey-and-Cinnamon-Milk-Drink','http://www.wikihow.com/Make-an-Iced-Latte','http://www.wikihow.com/Make-Kraft%C2%AE-Macaroni-and-Cheese','http://www.wikihow.com/Make-Cream-from-Milk','http://www.wikihow.com/Steam-Milk','http://www.wikihow.com/Make-Milk-Tea','http://www.wikihow.com/Make-a-Simple-Cheese-Sauce','http://www.wikihow.com/Make-Pastry-Cream','http://www.wikihow.com/Make-a-Flat-White-Coffee','http://www.wikihow.com/Cook-Tres-Leches-Cake', # dobj(Pour,Milk)
           'http://www.wikihow.com/Tame-a-Feral-Kitten','http://www.wikihow.com/Keep-a-Cat-from-Joining-You-in-Eating-a-Meal','http://www.wikihow.com/Measure-Salinity', # dobj(Move,Plate)
           'http://www.wikihow.com/Wrap-a-Box-With-a-Square-End','http://www.wikihow.com/Get-a-Litter-Trained-Cat-to-%22Go%22-Outside','http://www.wikihow.com/Litter-Train-a-Cat','http://www.wikihow.com/Create-a-Gravatar','http://www.wikihow.com/Pack-Boxes','http://www.wikihow.com/Move-out-Quickly', # dobj(Move,Box)
           'http://www.wikihow.com/Clean-a-Litter-Box','http://www.wikihow.com/Make-Molds-for-Plaster-Statues','http://www.wikihow.com/Clean-Your-Kitty-Litter-Box',
           'http://www.wikihow.com/Keep-Air-Out-of-Your-Baby\'s-Bottle', # dobj(Reach,Milk)
           'http://www.wikihow.com/Eat-Properly','http://www.wikihow.com/Eat-Healthy','http://www.wikihow.com/Eat-Like-a-Body-Builder','http://www.wikihow.com/Eat-and-Lose-Weight','http://www.wikihow.com/Improve-Your-Diet-(Teens)','http://www.wikihow.com/Eat-Less','http://www.wikihow.com/Eat-Clean-for-Life','http://www.wikihow.com/Eat-Healthy-and-Exercise','http://www.wikihow.com/Eat-Slowly','http://www.wikihow.com/Cope-With-Overeating','http://www.wikihow.com/Burn-Fat','http://www.wikihow.com/Eat-Small-Portions-During-Meals','http://www.wikihow.com/Stop-Food-Cravings-at-Night','http://www.wikihow.com/Have-a-Healthy-Pregnancy','http://www.wikihow.com/Diet-to-Lose-Weight-as-a-Teenage-Girl','http://www.wikihow.com/Identify-Trigger-Foods','http://www.wikihow.com/Lose-Weight-Safely', # nsubj(Eat,Person)
           'http://www.wikihow.com/Extinguish-an-Oil-Fire','http://www.wikihow.com/Protect-Valuables-on-the-Beach','http://www.wikihow.com/Wash-Dishes','http://www.wikihow.com/Make-a-Warm-Compress','http://www.wikihow.com/Wax','http://www.wikihow.com/Foundation-Piece-a-Quilt-Block','http://www.wikihow.com/Make-a-Mask','http://www.wikihow.com/Make-a-Ninja-Mask','http://www.wikihow.com/Polish-Stainless-Steel','http://www.wikihow.com/Make-Makeup','http://www.wikihow.com/Make-Cream-Cheese','http://www.wikihow.com/Drain-Sinuses', # dobj(Place,Cloth) 
           'http://www.wikihow.com/Play-Solitaire','http://www.wikihow.com/Bet-on-Soccer','http://www.wikihow.com/Make-Your-Bed','http://www.wikihow.com/Play-Craps','http://www.wikihow.com/Bid-on-eBay','http://www.wikihow.com/Place-Your-Fingers-Properly-on-Piano-Keys','http://www.wikihow.com/Shoot-Dice','http://www.wikihow.com/Play-Scrabble','http://www.wikihow.com/Play-Go','http://www.wikihow.com/Hug' # nsubj(Place,Person)   
        ]


#print len(URLList)

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
