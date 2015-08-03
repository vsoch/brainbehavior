from glob import glob

# Run iterations of "count" to count the number of terms in each folder of zipped up pubmed articles

topfolder = "/scratch/PI/russpold/data/PUBMED/articles"
subfolders = [os.path.basename(x) for x in glob("%s/*" %topfolder)]
outfolder = "/scratch/PI/russpold/data/PUBMED/counts"

# This pickle has a list of our terms
term_pickle =  "/scratch/PI/russpold/data/PUBMED/behavior_list.pkl"

for s in range(8000,len(subfolders)):
    subfolder = subfolders[s]
    jobfile = open(".job/%s.job" %subfolder,'w')
    jobfile.writelines("#!/bin/bash\n")
    jobfile.writelines("#SBATCH --job-name=%s_count.job\n" %(subfolder))
    jobfile.writelines("#SBATCH --output=.out/%s_count.out\n" %(subfolder))
    jobfile.writelines("#SBATCH --error=.out/%s_count.err\n" %(subfolder)) 
    jobfile.writelines("#SBATCH --time=2-00:00\n") 
    jobfile.writelines("#SBATCH --mem=12000\n")   
    jobfile.writelines("python /home/vsochat/SCRIPT/python/brainbehavior/analysis/pubmed/1.count.py %s %s %s %s\n" %(topfolder,subfolder,term_pickle,outfolder))  
    jobfile.close()
    os.system('sbatch -p russpold .job/%s.job' %subfolder)
