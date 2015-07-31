#!/usr/bin/env python2

# This script will launch instances of download_pubmed_muhaha.py

import os
from brainbehavior.pubmed import Pubmed

# First we need to download full article text
# Create a pubmed object
email = "vsochat@stanford.edu"
pm = Pubmed(email)

# Get pubmed ids for all articles in database
pc_ids = pm.get_pubmed_central_ids()

# Download folder
download_folder = "/scratch/PI/russpold/data/PUBMED/articles"

# Submit scripts to download in batches of 100
start = 0
iters = len(pc_ids)/100


# Find missing ones
missing = []
subfolders = []
for i in range(0,iters):
  print "%s of %s" %(i,iters)
  download_subfolder = "%s/%s" %(download_folder,i)
  start = i*100
  if i != iters: end = start + 100
  else: end = len(pc_ids)
  for ii in range(start,end):
      pmid = pc_ids[ii]
      if not check_download(pmid,download_subfolder):
          missing.append(pmid)
          subfolders.append(download_subfolder)

# Now submit missing jobs
for m in range(0,len(missing)):
  pmid = missing[m]
  download_folder = subfolders[m]
  jobname = "pm_%s" %(pmid)
  filey = open(".job/%s.job" % (jobname),"w")
  filey.writelines("#!/bin/bash\n")
  filey.writelines("#SBATCH --job-name=%s\n" %(jobname))
  filey.writelines("#SBATCH --output=.out/%s.out\n" %(jobname))
  filey.writelines("#SBATCH --error=.out/%s.err\n" %(jobname))
  filey.writelines("#SBATCH --time=2-00:00\n")
  filey.writelines("#SBATCH --mem=12000\n")
  filey.writelines("python /home/vsochat/SCRIPT/python/brainbehavior/analysis/pubmed/download_pubmed_single.py %s %s %s\n" % (pmid,download_subfolder,email))
  filey.close()
  os.system("sbatch -p russpold .job/%s.job" % (jobname))
