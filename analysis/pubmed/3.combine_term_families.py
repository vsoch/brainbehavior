from brainbehavior.cognitiveatlas import load_behaviors, Behavior, get_json, get_term_strings, get_term_objects, get_path_similarity_matrix
from brainbehavior.utils import save_json
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
synset_selection_file = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/brainbehavior/data/cognitiveatlas/term_synsets.txt"
synsets = pandas.read_csv(synset_selection_file,sep="\t")
synset_selection = dict()
for row in synsets.iterrows():
    synset_selection[row[1].term] = row[1].synset

path_similarities = get_path_similarity_matrix(behaviors,synset_selection)

# Step 2: For each term, find family based on path similarity
for bname,sname in synset_selection.iteritems():
    if isinstance(sname,str):
        family = path_similarities[sname][path_similarities[sname] != 0]
    else:
    #STOPPED HERE - write this function when new matrix is generated!
