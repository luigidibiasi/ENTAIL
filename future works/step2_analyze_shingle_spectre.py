#This script computes the DCDB descriptors
#
#The DCDB descriptor form is:
#
#
# L-Shingle-Pos



MAX_KMER = 3
DCDB = {}
MATRIX = {}
TOT_SEQ=0
with open("./union.txt") as reader:
    #skip header
    reader.readline()
    #extract every length
    for seqX in reader:
        seq=seqX
        seq = seq.split('\t')[0]
        target = seqX.split('\t')[25]
        target=target.replace('\n','')
        TOT_SEQ+=1

        i = 0
        s = 0
        seq_len=len(seq)
        # how many step
        for s in range (1,MAX_KMER+1):
            for i in range (0,(seq_len-s)+1):
                kmer = seq[i:i+s]
                dcdb = kmer+str(i)        
                if (not dcdb in DCDB):
                    DCDB[dcdb]={}
                if (not target in DCDB[dcdb]):
                    DCDB[dcdb][target]=0
                DCDB[dcdb][target]+=1
            

print("Extracting SPECTRE")
with open("./dcdb_spectre.tsv","w") as writer:
    writer.write("DESCR\tPYES\tPNO\n")
    for dcdb in DCDB:
        if ("Yes" in DCDB[dcdb] and "No" in DCDB[dcdb]):
            writer.write(dcdb +"\t")
            writer.write(str((DCDB[dcdb]["Yes"]/TOT_SEQ)*100)+"\t")
            writer.write(str((DCDB[dcdb]["No"]/TOT_SEQ)*100)+"\n")
exit()
print("Extracting MATRIX")
