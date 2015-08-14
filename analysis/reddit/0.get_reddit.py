from brainbehavior.cognitiveatlas import get_expanded_family_dict, get_path_similarity_matrix
from brainbehavior.nlp import get_term_counts, do_stem, get_total_words
from glob import glob
import pandas
import pickle
import praw
import pickle
from glob import glob
import pandas
import sys
import os

r = praw.Reddit(user_agent='cogatpheno')

### 1. GET REDDIT CONTENT ##################################################################
# Read in list of disorders to search for
disorders = ["depression","anxiety","stress","OCD","panic","phobia","PTSD",
             "EatingDisorders","autism","amnesia","Alzheimers","BipolarReddit",
             "schizophrenia","narcissism","narcolepsy","Drug_Addiction"]

redditdict = dict()

for disorder in disorders:
    print "Parsing %s" %disorder
    submissions = r.get_subreddit(disorder).get_hot(limit=1000)
    content = []
    for sub in submissions:
        content.append(sub.selftext)
    redditdict[disorder] = content

pickle.dump(redditdict,open("analysis/reddit/disorder_dict.pkl","wb"))


### 2. COUNT TERMS ##################################################################
term_pickle = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/brainbehavior/data/cognitiveatlas/behavioraltraits.pkl"
terms = pickle.load(open(term_pickle,"rb"))
stems = do_stem(terms)

countdfs = dict()

for disorder,content in redditdict.iteritems():    
    print "Parsing %s" %disorder
    # We will save counts and total words
    dfcount = pandas.DataFrame(columns=stems)
    totalwords = []
    # We want to keep a count of those with no terms
    noterms = 0
    for t in range(0,len(content)):
        text = ''.join([i if ord(i) < 128 else ' ' for i in content[t]])
        counts = get_term_counts(terms,str(text))
        # Only save if we have at least one!
        if counts["count"].sum() > 0:    
            totalwords.append(get_total_words(text))
            dfcount.loc[t,counts.index] = counts["count"]
    countdfs[disorder] = {"df":dfcount,"words":totalwords}

# Save to output file
pickle.dump(countsdf,open("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/reddit/countdfsreddit.pkl","wb"))

### 3. COMBINE COUNTS BY FAMILY ##############################################################
# Prepare behavioral terms
families = get_expanded_family_dict(unique=True)

# This is NOT a diagonal matrix, base terms are in rows, family members in columns
path_similarities = get_path_similarity_matrix()

for disorder,data in countdfs.iteritems():
    result = data["df"]

    # This will be a new matrix with only base terms as column names
    familydf = pandas.DataFrame(index=result.index)

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
    familydf.to_pickle("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/reddit/result/%s_familydf.pkl" %disorder)

### 4. CO-OCCURRENCE ##################################################################
    # Now calculate co-occurrence
    terms = familydf.columns.tolist()

    # Result df will be terms by terms
    df = pandas.DataFrame(columns=terms,index=terms)

    for t in range(0,len(terms)):
        print "%s of %s" %(t,len(terms))
        term1 = terms[t]
        subset = familydf.loc[familydf[term1]>0]
        number_with_term1 = subset.shape[0]
        if number_with_term1 != 0:
            for term2 in terms:
                number_with_term2 = subset[term2].loc[subset[term2]>0].shape[0]
                pt2_given_t1 = float(number_with_term2) / number_with_term1
                # [row](probability), [col](given)
                df.loc[term2,term1] = pt2_given_t1    
        else:
            df.loc[:,term1] = 0

    df.to_csv("/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/reddit/result/%s_co-occurrence.tsv" %disorder,sep="\t")

