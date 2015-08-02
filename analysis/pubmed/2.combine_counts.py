from glob import glob
import pandas
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

for f in range(0,len(files)):
    print "%s of %s" %(f,len(files))
    input_folder = files[f]
    count = pickle.load(open(input_folder,"rb"))
    counts = counts.append(count["df"])
    total_words.append(count["total_words"])
    files_in_folder.append(count["files_in_folder"])
    noterms_count.append(count["noterms_count"])


# Save to file
result = {"counts":counts,
         "total_words":total_words,
         "files_in_folder":files_in_folder,
         "noterms_count":noterms_count}
pickle.dump(result,open("%s/pmc_counts_result.pkl" %output_folder,"wb"))


