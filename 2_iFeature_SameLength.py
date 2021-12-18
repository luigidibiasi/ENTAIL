# This script executes iFeatures for the training dataset
import os


#build iFeature input
print("Preparing iFeature input...")
with open("./input_iFeatures.txt","w") as writer:
    with open("./BALANCED_1032_LEN6_INPUT_SEQUENCES.csv") as reader:
        reader.readline()
        for l in reader:
            lData = l.split("\t")
            seq = lData[0]
            writer.write(">"+str(seq)+"\n")
            writer.write(str(seq)+"\n")

#Extract descriptor that allows different length
print("Preparing descriptors...")
descr = ["QSOrder","SOCNumber","APAAC","PAAC","CKSAAGP","CKSAAP","NMBroto","Geary","Moran","BINARY","EAAC","AAINDEX","ZSCALE","BLOSUM62","EGAAC","AAC","DPC","DDE","TPC","GAAC","GDPC","GTPC","CTDC","CTDT","CTDD","CTriad","KSCTriad"]
for d in descr:
    try:
        b = os.path.getsize("./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/"+str(d)+".txt")
    except:
        b=0
    if (b<=30):
        print("Executing " + d);
        if (d=="Moran" or d=="Geary" or d=="NMBroto"):
            os.system('python ../iFeature/codes/'+d+'.py --file ./input_iFeatures.txt --nlag 5 --out ./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/'+str(d)+'.txt')
        else:
            if(d=="CKSAAP" or d=="CKSAAGP"):
                os.system('python ../iFeature/codes/'+d+'.py ./input_iFeatures.txt 4 ./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/'+str(d)+'.txt')
            else:
                if(d=="PAAC" or d=="APAAC" or d=="SOCNumber" or d=="QSOrder"):
                    os.system('python ../iFeature/codes/'+d+'.py ./input_iFeatures.txt 5 ./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/'+str(d)+'.txt')
                    print('python ../iFeature/codes/'+d+'.py ./input_iFeatures.txt 5 ./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/'+str(d)+'.txt')
                else:
                    os.system('python ../iFeature/iFeature.py --file ./input_iFeatures.txt --type '+str(d)+' --out ./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/'+str(d)+'.txt')
                    print('python ../iFeature/iFeature.py --file ./input_iFeatures.txt --type '+str(d)+' --out ./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/'+str(d)+'.txt')        

print("Done!")



#"KNNprotein" how to use?
#"KNNpeptide"
#SSEC
#"TA"
#"ASA"
#"PSSM"
#SSEC
#SSEB
#"Disorder","DisorderC","DisorderB"           

