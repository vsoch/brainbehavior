library(reshape)
library(plyr)
library(pheatmap)

indir = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/reddit/result/v2/co-occurrence"
input_datas = list.files(indir,pattern="*.tsv")
outdir = "/home/vanessa/Documents/Dropbox/Code/Python/brain-behavior/analysis/reddit/web/v2"

for (input_data in input_datas){
    input_file = paste(indir,"/",input_data,sep="")
    output_file = paste(outdir,"/",input_data,sep="")  
    df = read.csv(input_file,sep="\t",row.names=1)  
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
    write.table(flat,file=output_file,sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)    
}



# We need labels manually embedded in html
cat(rownames(df),sep='","')