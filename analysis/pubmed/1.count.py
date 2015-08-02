from brainbehavior.pubmed import get_xml_tree
from brainbehavior.cognitiveatlas import get_behaviors
from brainbehavior.nlp import get_term_counts, do_stem, get_total_words
from glob import glob
import pandas
import pickle
import sys

# Here is the path to the folder with xml files
topfolder = sys.argv[1]
subfolder = sys.argv[2]
term_pickle = sys.argv[3]
outfolder = sys.argv[4]

folder = "%s/%s" %(topfolder,subfolder)

# Get compressed files in folder.
zips = glob("%s/*.tar.gz" %folder)

# Read in our terms
terms = pickle.load(open(term_pickle,"rb"))
stems = do_stem(terms)

# We will save counts and total words
dfcount = pandas.DataFrame(columns=stems)
totalwords = []


# We want to keep a count of those with no terms
noterms = 0

for z in zips:
    zname = "%s/%s" %(subfolder,os.path.basename(z))
    text = get_xml_tree(z)
    # Only save if we have at least one!
    if counts["count"].sum() > 0:
        counts = get_term_counts(terms,text)
        totalwords.append(get_total_words(text))
        df.loc[zname,counts.index] = counts["count"]
    else noterms += 1

# Save to output file
result = {df:df,noterms_count:noterms,files_in_folder:len(zips),total_words=totalwords}
pickle.dump(result,open("%s/%s_counts.pkl" %(outfolder,subfolder)),"wb")
