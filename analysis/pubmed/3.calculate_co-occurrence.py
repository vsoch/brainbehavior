from glob import glob
import pandas
import pickle

# NOTE: this will likely need to be run on a bigmem node...

input_pickle = "/scratch/PI/russpold/data/PUBMED/pmc_counts_result.pkl"
result = pickle.load(open(input_pickle,"rb"))

terms = result["counts"].columns.tolist()
articles = result["counts"].index.tolist()

# Result df will be terms by terms
df = pandas.DataFrame(columns=terms,index=terms)

for t in range(0,len(terms)):
    print "%s of %s" %(t,len(terms))
    term1 = terms[t]
    subset = result["counts"].loc[result["counts"][term1]>0]
    number_with_term1 = subset.shape[0]
    if number_with_term1 != 0:
        for term2 in terms:
            number_with_term2 = subset[term2].loc[subset[term2]>0].shape[0]
            pt2_given_t1 = float(number_with_term2) / number_with_term1
            # [row](probability), [col](given)
            df.loc[term2,term1] = pt2_given_t1    
    else:
        df.loc[:,term1] = 0
