#!/usr/bin/env python2

# This script will use the brainbehavior.py module to parse a text corpus for a list of terms
# For example, wikipedia, this script was not used for main (pubmed) analysis
from brainbehavior.wikipedia import get_page_content, get_headers, get_section_text
from brainbehavior.nlp import get_term_counts
import pickle

# Step 1: Read in behavioral term list (generated with 1.create_ontology
output_folder = "/home/vanessa/Documents/Dropbox/Website/traits/data"
terms = pickle.load(open("%s/behavior_list.pkl" %(output_folder),"rb"))

# Step 2: Get data from an "expert source" - let's start with wikipedia!
test_disorder = "major depressive disorder"
text = get_page_content(test_disorder)

# Get the section text to parse!
headers = get_headers(text)
sections = headers[0:2] # [u'== Symptoms and signs ==', u'=== Comorbidity ===']
section_text = get_section_text(text,sections)

# First let's try just term counts
counts = get_term_counts(terms=terms,text=section_text)

#Boom! Works! Now to do for a larger set...

# 5. Parse some corpus, and break into papers about disorders that we have in RDoC, cognitive atlas, and behavioral data.


# 6. For each term in ontology, take simple counts to calculate the probability of the term given the disorder. (or probabiliy of term1 given term2 in title (meaning the literature is "about" that term))
# 7. We may want to do something more intelligent like parsing individual sentences and breaking into parts of speech, determining some kind of more detailed relationship about terms (other than co-occurence). Will determine this when I get there.
# 8. Finished ontology should be explorable in web interface, define how behavioral traits are related (definition wise), and how they are related in the literature (based on disorders). We can then extend to actual behavioral data.
