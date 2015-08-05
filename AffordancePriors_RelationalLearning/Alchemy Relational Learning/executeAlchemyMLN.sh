cd ~/Downloads/alchemy-2/bin
./learnwts -i ../exdata/vishal-test/SVOPredicateFormula.mln -o ../exdata/vishal-test/learnwts.mln -t ../exdata/vishal-test/SVOTuples.db -ne nsubj, dobj -noAddUnitClauses
echo verb = {Wash,Prefer,Get,Use,Remove,See,Cook,S,Peel,Bathe,Leaves,Infuse,Find,Keep,Putting,Cut,Sprinkle,Have,Make,Add,Enjoy,Sweet,Stop,Smelly,Put,Pour,Dried,Peels,Freshen,Best,Place,Bag,Create,Addition,Degrade,Claim,Slows,Has,Myth,Judge,Is,Digging,Chew,Substitute,Simmering,Ward,Rub,Start,Bothering,Causing,Problems,Citrus,Dry,Turns,Coarsely,Potpourri,Be,Grub,Leave,Unsuitable,Stabilized,Using,M,Move,Require,Placing,Wagons,Maneuver,Discharging,Determines,Wet,Meet,Suffers,Hot,Allow,Expand,Collect,Determine,Perform,Contribute,Set,Affect,Increase,Will,Arrive,Let,Troweling,Checking,Full,Are,Requires,Check} >> ../exdata/vishal-test/learnwts.mln
./infer -p -i ../exdata/vishal-test/learnwts.mln -r ../exdata/vishal-test/inference.mln -e ../exdata/vishal-test/empty.db -q nsubj, dobj