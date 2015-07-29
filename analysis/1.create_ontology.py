#!/usr/bin/env python2

# This script will use the brainbehavior.py module to search for behavioral terms in
# relevant paper abstracts, and return a matrix of disorder ids (columns) by papers (rows)
# with "1" indicating that a disorder term was found, and "0" not.
from brainbehavior.cognitiveatlas import load_behaviors, Behavior, get_json, get_term_strings
from brainbehavior.utils import save_json

# Step 1: Read in behavioral terms
traits = load_behaviors()

# Step 2: For each term, generate behavior object with "is_a" relationships
behaviors = []
for trait in traits:
    behaviors.append(Behavior(trait))

# Step 3: Generate a json for each trait that shows relationships
output_folder = "/home/vanessa/Documents/Dropbox/Website/traits/data"
sim_metrics = ["path","lch","wup"]

for sim_metric in sim_metrics:
    for behavior in behaviors:
        myjson = behavior.get_json()
        save_json(myjson,"%s/%s/behaviors_%s.json" %(output_folder,sim_metric,behavior.trait))

for sim_metric in sim_metrics:
    myjson = get_json(behaviors,sim_metric=sim_metric)
    save_json(myjson,"%s/behaviors_%s.json" %(output_folder,sim_metric))


# 4. Create database of terms, and visualize ontology (done)
# http://www.vbmis.com/bmi/project/traits

# 5. Get list of unique strings to use to parse text
terms = get_term_strings(behaviors)
pickle.dump(terms,open("%s/behavior_list.pkl" %(output_folder),"wb"))
