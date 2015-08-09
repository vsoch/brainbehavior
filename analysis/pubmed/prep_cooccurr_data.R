library(reshape)
library(plyr)

input_data = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/pubmed/pmc_family_co-occurrence.tsv"
outdir = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/pubmed"

df = read.csv(input_data,sep="\t")
rownames(df) = df[,1]
df = df[,-1]

# Remove rows/cols where we didn't find at all
df = df[which(rowSums(df) != 0),]
df = df[,which(colSums(df) != 0)]

outputfile = paste(outdir,"/web/co-occurrence.tsv",sep="")

# Melt into data frame
flat = melt(as.matrix(df))
x = c()
y = c()
for (dx in 1:nrow(df)){
  for (dy in 1:ncol(df)){
   x = c(x,dx)
   y = c(y,dy)
  }
}
flat$x = x
flat$y = y
colnames(flat) = c("probof","given","prob","x","y")
write.table(flat,file=outputfile,sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)

# We need labels manually embedded in html
cat(rownames(df),sep='","')
