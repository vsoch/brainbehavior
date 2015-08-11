# if on sherlock, need to load python2.7
# module load python/2.7.5
from brainbehavior.cognitiveatlas import get_expanded_family_dict, get_path_similarity_matrix
#from brainbehavior.utils import save_json
from brainbehavior.nlp import do_stem
#from textblob.wordnet import Synset
from glob import glob
import pandas
import pickle

# We want to first generate a matrix of relationships between all pairwise terms
families = get_expanded_family_dict()

# This is NOT a diagonal matrix, base terms are in rows, family members in columns
path_similarities = get_path_similarity_matrix(families)

# Load the result
result = pandas.read_pickle("/share/PI/russpold/work/PUBMED/pmc_behavior_counts.pkl")

# Step 1: Terms that appear in most papers need to be filterd out
percents = []
for c in result.columns:
    col = result[c]
    percent_occur = col[col!=0].shape[0] / float(col.shape[0])
    percents.append(percent_occur)
percents = pandas.DataFrame(percents)
percents.index = result.columns
percents.to_csv("/share/PI/russpold/work/PUBMED/pmc_percent_occur.tsv",sep="\t")

# Lets try nixing words with > 0.4 frequency...
nix = percents.loc[percents[0]>0.1]
result[nix.index] = 0

# This will be a new matrix with only base terms as column names
familydf = pandas.DataFrame(index=result.index)

# Get the unique family dictionary
families = get_expanded_family_dict(unique=True)

# Step 2: For each term stem (row), find family based on path similarity
for stem,data in families.iteritems():
    family = path_similarities[stem][path_similarities[stem] != 0]
    # Create a data frame with just the columns
    column_names = [c for c in family.index if c in result.columns]
    family = family[column_names]
    # if there are no family members
    if family.shape[0] == 0: 
        familydf[stem] = result[stem]
    # Weight each count by the path similarity, and sum
    else:
        subset = result[column_names].copy()
        for col in subset.columns:
            subset[col] *= family[col]
        familydf[stem] = subset.sum(axis=1) + result[stem]
    
# Save family data frame to file
familydf.to_pickle("/share/PI/russpold/work/PUBMED/behavior_family_df_filtered_pt1.pkl")
