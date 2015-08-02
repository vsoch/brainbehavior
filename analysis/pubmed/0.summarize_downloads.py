#!/usr/bin/env python2
# We want to know, of the files we have, what is the breakdown?


import os
import pandas
from brainbehavior.pubmed import Pubmed

# First we need to download full article text
# Create a pubmed object
email = "vsochat@stanford.edu"
pm = Pubmed(email)

# Get pubmed ids for all articles in database
pc_ids = pm.get_pubmed_central_ids()

# We are going to download them here
download_folder = "/scratch/PI/russpold/data/PUBMED/articles"

# Submit scripts to download in batches of 100
iters = len(pc_ids)/100

# Subset matrix to files we have downloaded
subset = pandas.DataFrame(columns=pm.ftp.columns)

for i in range(0,iters):
    print "%s of %s" %(i,iters)
    download_subfolder = "%s/%s" %(download_folder,i)
    start = i*100
    if i != iters:
        end = start + 100
    else:
        end = len(pc_ids)
    # Which paths exist?
    idx = [ x[0] for x in pm.ftp.loc[start:end].iterrows() if os.path.exists("%s/%s" %(download_subfolder,os.path.basename(x[1]["URL"])))]
    subset = subset.append(pm.ftp.loc[idx])

# How many?
subset.shape[0]
pm.ftp.shape[0] - subset.shape[0]

# Now count journals
subset["JOURNAL_NAME"] = [x.split(".")[0] for x in subset["JOURNAL"]]
counts = subset["JOURNAL_NAME"].value_counts()
counts.to_pickle("%s/journal_counts.pkl" %download_folder)


