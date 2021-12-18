#This script computes the DCDB descriptors
#
#The DCDB descriptor form is:
#
#
# L-Shingle-Pos



MAX_KMER = 2
DCDB = {}
MATRIX = {}
with open("./union.txt") as reader:
    #skip header
    reader.readline()
    #extract every length
    for seqX in reader:
        seq=seqX
        seq = seq.split('\t')[0]
        target = seqX.split('\t')[25]
        target=target.replace('\n','')        
        
        
        seq_len = len(seq)

        i = 0
        s = 0

        MATRIX[seq]={}
        
        # how many step
        for s in range (1,MAX_KMER+1):
            for i in range (0,(seq_len-s)+1):
                kmer = seq[i:i+s]
                dcdb = kmer+str(i)
                if (not dcdb in DCDB):
                    DCDB[dcdb]=0                
                DCDB[dcdb]+=1                
                MATRIX[seq][dcdb]=1

print("Extracting SPECTRE")
with open("./dcdb_spectre.tsv","w") as writer:
    writer.write("DESCR\tVAL\n")
    for dcdb in DCDB:
        writer.write(dcdb +"\t"+str(DCDB[dcdb])+"\n")
print("Extracting MATRIX")

with open("./DCDB.tsv","w") as writer:
    #write the header
    writer.write("SEQ\t")
    for dcdb in DCDB:
        writer.write(dcdb+"\t")
    writer.write("TARGET\n")
    with open("./union.txt") as reader:
        #skip header
        reader.readline()
        for seq in reader:
            seq=seq.replace("\n","")            
            s = seq.split("\t")[0]
            v = seq.split("\t")[25]            
            writer.write(s+"\t")
            for dcdb in DCDB:
                if (dcdb in MATRIX[s]):
                    writer.write("1\t")
                else:
                    writer.write("0\t")
            writer.write(v+"\n")
            writer.flush()
        print("finito")
        exit()
    
        


