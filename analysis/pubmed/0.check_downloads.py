#!/usr/bin/env python2

# This script will launch instances of download_pubmed_muhaha.py

import os
import time
from brainbehavior.pubmed import Pubmed
from glob import glob

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

# Function to submit a single iteration of a missing job
def submit_single_missing(pmid,download_folder,email):
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

# Delete repeat files
for i in range(0,iters):
  download_subfolder = "%s/%s" %(download_folder,i)
  extra_files = glob("%s/*.tar.gz.*" %(download_subfolder))
  if len(extra_files) > 0:
      print "%s extra files" %extra_files
      [os.remove(x) for x in extra_files]

# First find folders that don't have 100 files
folders = []
its= []
numbers = []
for i in range(0,iters):
  print "%s of %s" %(i,iters)
  download_subfolder = "%s/%s" %(download_folder,i)
  number_files = len(glob("%s/*.tar.gz"%download_subfolder))
  if number_files < 100:
    folders.append(download_subfolder)
    its.append(i)
    numbers.append(number_files)
  

# Submit for entire folder (using Pubmed ftp)
for f in range(0,len(its)):
    i = its[f]  
    print "%s of %s" %(i,iters)
    download_subfolder = "%s/%s" %(download_folder,i)
    start = i*100
    if i != iters: end = start + 100
    else: end = len(pc_ids)
    jobname = "pm_%s-%s" %(start,end)
    filey = open(".job/%s.job" % (jobname),"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=%s\n" %(jobname))
    filey.writelines("#SBATCH --output=.out/%s.out\n" %(jobname))
    filey.writelines("#SBATCH --error=.out/%s.err\n" %(jobname))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=12000\n")
    filey.writelines("python /home/vsochat/SCRIPT/python/brainbehavior/analysis/pubmed/download_pubmed_muhaha.py %s %s %s %s\n" % (start,end,download_subfolder,email))
    filey.close()
    os.system("sbatch -p russpold .job/%s.job" % (jobname))


# Submit for entire folder (using pubmed pickles, local)
ids_pickle = "/scratch/PI/russpold/data/PUBMED/pmc_ids.pkl"
ftp_pickle = "/scratch/PI/russpold/data/PUBMED/ftp_df.pkl"

for f in range(6800,len(its)):
    i = its[f]  
    print "%s of %s" %(i,iters)
    download_subfolder = "%s/%s" %(download_folder,i)
    start = i*100
    if i != iters: end = start + 100
    else: end = len(pc_ids)
    jobname = "pm_%s-%s" %(start,end)
    filey = open(".job/%s.job" % (jobname),"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=%s\n" %(jobname))
    filey.writelines("#SBATCH --output=.out/%s.out\n" %(jobname))
    filey.writelines("#SBATCH --error=.out/%s.err\n" %(jobname))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=12000\n")
    filey.writelines("python /home/vsochat/SCRIPT/python/brainbehavior/analysis/pubmed/download_pubmed_local.py %s %s %s %s %s\n" % (start,end,download_subfolder,ftp_pickle,ids_pickle))
    filey.close()
    os.system("sbatch -p russpold .job/%s.job" % (jobname))

# Now find missing files in folders, submit single missing jobs
for f in range(0,len(its)):
  i = its[f]  
  print "%s of %s" %(i,iters)
  download_subfolder = "%s/%s" %(download_folder,i)
  start = i*100
  if i != iters: end = start + 100
  else: end = len(pc_ids)
  for ii in range(start,end):
      pmid = pc_ids[ii]
      if not pm.check_download(pmid,download_subfolder):
          print "Missing %s" %pmid
          submit_single_missing(pmid,download_subfolder,email)
                  

submit = False
          while submit == False:
              numberjobs = int(os.popen("squeue -u vsochat|wc -l").read().strip("\n"))
              while numberjobs < 5000:
                  numberjobs = int(os.popen("squeue -u vsochat|wc -l").read().strip("\n"))
         
