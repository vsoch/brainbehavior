from brainbehavior.pubmed import get_xml_tree
from brainbehavior.cognitiveatlas import get_behaviors
from brainbehavior.nlp import get_term_counts, do_stem
from glob import glob
import pandas
import pickle
import sys

# Here is the path to the folder with xml files
topfolder = sys.argv[1]
subfolder = sys.argv[2]
term_pickle = sys.argv[3]

folder = "%s/%s" %(topfolder,subfolder)

# Get compressed files in folder.
zips = glob("%s/*.tar.gz" %folder)

# Read in our terms
terms = pickle.load(open(term_pickle,"rb"))
stems = do_stem(terms)

# We will save in a pandas data frame
df = pandas.DataFrame(columns=stems)

for z in zips:
    zname = "%s/%s" %(subfolder,os.path.basename(z))
    text = get_xml_tree(z)
    # Only save if we have at least one!
    if counts["count"].sum() > 0:
        counts = get_term_counts(terms,text)
        df.loc[zname,counts.index] = counts["count"]

# Save to output file
df.to_pickle("%s/%s_counts.pkl" %(folder,subfolder))
