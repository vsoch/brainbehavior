import os

# Read in list of disorders to search for
disorders = ["depression","anxiety","stress","OCD","panic","phobia","PTSD",
             "EatingDisorders","autism","amnesia","Alzheimers","BipolarReddit",
             "schizophrenia","narcissism","narcolepsy","Drug_Addiction","relationships",
             "gaming","worldnews","politics","movies","science","atheism","Showerthoughts",
             "cringe","rage","niceguys","sex","loseit","raisedbynarcissists","BPD",
             "AvPD","DID","SPD","EOOD","CompulsiveSkinPicking","psychoticreddit","insomnia"]

outfolder = "/share/PI/russpold/work/REDDIT/content"

for disorder in disorders:
    if not os.path.exists("%s/%s_dict.pkl" %(outfolder,disorder)):
        jobfile = open(".job/%s.job" %disorder,'w')
        jobfile.writelines("#!/bin/bash\n")
        jobfile.writelines("#SBATCH --job-name=%s_reddit.job\n" %(disorder))
        jobfile.writelines("#SBATCH --output=.out/%s_reddit.out\n" %(disorder))
        jobfile.writelines("#SBATCH --error=.out/%s_reddit.err\n" %(disorder)) 
        jobfile.writelines("#SBATCH --time=2-00:00\n") 
        jobfile.writelines("#SBATCH --mem=12000\n")   
        jobfile.writelines("python /home/vsochat/SCRIPT/brainbehavior/analysis/reddit/parse_reddit.py %s %s\n" %(disorder,outfolder))  
        jobfile.close()
        os.system('sbatch -p russpold .job/%s.job' %disorder)
