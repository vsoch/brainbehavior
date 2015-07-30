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

# We are going to download them here
download_folder = "/scratch/PI/russpold/DATA/PUBMED/articles"

# Submit scripts to download in batches of 100
start = 0
iters = len(pc_ids)/100

# Prepare and submit a job for each
for i in range(0,5000):
  download_subfolder = "%s/%s" %(download_folder,i)
  if not os.path.exists(download_subfolder):
      os.mkdir(download_subfolder)
  start = i*100
  if i != iters:
    end = start + 100
  else:
    end = len(pc_ids)
if 1==1:
  jobname = "pm_%s-%s" %(start,end)
  filey = open(".job/%s.job" % (jobname),"w")
  filey.writelines("#!/bin/bash\n")
  filey.writelines("#SBATCH --job-name=%s\n" %(jobname))
  filey.writelines("#SBATCH --output=.out/%s.out\n" %(jobname))
  filey.writelines("#SBATCH --error=.out/%s.err\n" %(jobname))
  filey.writelines("#SBATCH --time=2-00:00\n")
  filey.writelines("#SBATCH --mem=12000\n")
  # Usage : download_pubmed_muhaha.py start end download_folder
  filey.writelines("python /home/vsochat/SCRIPT/python/brainbehavior/analysis/pubmed/download_pubmed_muhaha.py %s %s %s %s\n" % (start,end,download_subfolder,email))
  filey.close()
  os.system("sbatch -p russpold .job/%s.job" % (jobname))
