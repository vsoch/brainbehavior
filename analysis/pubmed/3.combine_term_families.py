# if on sherlock, need to load python2.7
# module load python/2.7.5
from brainbehavior.cognitiveatlas import load_behaviors, Behavior, get_json, get_term_strings, get_term_objects, get_path_similarity_matrix
from brainbehavior.utils import save_json
from brainbehavior.nlp import do_stem
from textblob.wordnet import Synset
from glob import glob
import pandas
import pickle

# We want to first generate a matrix of relationships between all pairwise terms

input_pickle = "/scratch/PI/russpold/data/PUBMED/pmc_counts_pandas_df.pkl"
result = pandas.read_pickle(input_pickle)

# Step 1: Generate matrix that calculate pairwise path distances
traits = load_behaviors()
behaviors = []
for trait in traits:
    behaviors.append(Behavior(trait))

# Read in the synset selection file - into a dictionary to look up based on name
synset_selection_file = "/home/vsochat/SCRIPT/python/brainbehavior/brainbehavior/data/cognitiveatlas/term_synsets.txt"
synsets = pandas.read_csv(synset_selection_file,sep="\t")
synset_selection = dict()
for row in synsets.iterrows():
    synset_selection[row[1].term] = row[1].synset

path_similarities = get_path_similarity_matrix(behaviors,synset_selection)

# Do some manual work to fix columns

# Step 2: For each term, find family based on path similarity
used = [] 
for bname,sname in synset_selection.iteritems():
    if isinstance(sname,str):
        family = path_similarities[sname][path_similarities[sname] != 0]
        # Add names to list, to check for overlap
        used = used + family.index.tolist()
        column_names = do_stem([x.split(".")[0] for x in family.index.tolist()])
        family.index = column_names
        # Create a data frame with just the columns
        column_names = [c for c in column_names if c in result.columns]
        family = family[column_names]
        subset = result[]
    else:
    #STOPPED HERE - write this function when new matrix is generated!


