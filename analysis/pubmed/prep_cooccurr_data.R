library(reshape)
library(plyr)

input_data = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/pubmed/pmc_family_co-occurrence.tsv"
outdir = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/pubmed"

df = read.csv(input_data,sep="\t")
rownames(df) = df[,1]
df = df[,-1]

outputfile = paste(outdir,"/co-occurrence.tsv",sep="")

# Melt into data frame
flat = melt(as.matrix(df))
flat$x = 1:nrow(df)
flat$y = 1:ncol(df)
colnames(flat) = c("probof","given","prob","x","y")
write.table(flat,file=outputfile,sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)
