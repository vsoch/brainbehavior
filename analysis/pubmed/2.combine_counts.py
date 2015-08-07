from glob import glob
import pandas
import numpy
import pickle

# NOTE: this will likely need to be run on a bigmem node...

input_folder = "/scratch/PI/russpold/data/PUBMED/counts"
output_folder = "/scratch/PI/russpold/data/PUBMED"
files = glob("%s/*.pkl" %input_folder)
tmp = pickle.load(open(files[0],"rb"))

# Save counts dataframe, total words, and missing
counts = pandas.DataFrame(columns=tmp["df"].columns)
total_words = []
files_in_folder = []
noterms_count = []

# Function to Save to file
def save_result(counts,total_words,files_in_folder,noterms_count):
    result = {"counts":counts,
         "total_words":total_words,
         "files_in_folder":files_in_folder,
         "noterms_count":noterms_count}
    pickle.dump(result,open("%s/pmc_counts_result.pkl" %output_folder,"wb"))


for f in range(0,len(files)):
    print "%s of %s" %(f,len(files))
    input_folder = files[f]
    count = pickle.load(open(input_folder,"rb"))
    counts = counts.append(count["df"])
    total_words.append(count["total_words"])
    files_in_folder.append(count["files_in_folder"])
    noterms_count.append(count["noterms_count"])
    if f % 1000 == 0:
        save_result(counts,total_words,files_in_folder,noterms_count)

save_result(counts,total_words,files_in_folder,noterms_count)

# What is average total words?
#numpy.mean(total_words)
#numpy.sum(noterms_count)

# Save total words and files_in_folder
pickle.dump(total_words,open("%s/pmc_total_words.pkl" %output_folder,"wb"))
pickle.dump(noterms_count,open("%s/pmc_noterms_count.pkl" %output_folder,"wb"))

# Save just the dataframe (likely better compression this way)
# counts.to_pickle("%s/pmc_counts_pandas_df.pkl" %output_folder)
# This doesn't work - try hd5 store
counts.to_hdf("%s/pmc_counts_pandas_df.h5" %output_folder,'df',append=True)
counts.to_sql()
