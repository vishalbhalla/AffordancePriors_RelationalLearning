cd ~/Downloads/alchemy-2/bin
./learnwts -g -i ../exdata/vishal-test/SVOPredicateFormula.mln -o ../exdata/vishal-test/learnwts.mln -t ../exdata/vishal-test/SVOTuples.db -noAddUnitClauses
echo verb = {Reach,Open,Move,Place,Contain,Close,Eat,Drink,Pour,Clean,} >> ../exdata/vishal-test/learnwts.mln
./infer -p -i ../exdata/vishal-test/learnwts.mln -r ../exdata/vishal-test/inference.mln -e ../exdata/vishal-test/empty.db -q nsubj,dobj