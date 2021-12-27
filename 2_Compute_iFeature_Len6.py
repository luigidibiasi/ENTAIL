# This script executes iFeatures for the training dataset
import os
from src.common import *

TRAINING_SET = "TESTSET_BALANCED_400_input_sequences"


#build iFeature input
print("Preparing iFeature input...")
with open(SWAP_PATH +"/input_iFeatures.txt","w") as writer:
    with open(TRAINING_PATH + "/"+TRAINING_SET+".csv") as reader:
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
        b = os.path.getsize("./descriptors/"+TRAINING_SET+"/"+str(d)+".txt")
    except:
        b=0
    if (b<=30):
        print("Executing " + d);
        if (d=="Moran" or d=="Geary" or d=="NMBroto"):
            os.system('python ./iFeature/codes/'+d+'.py --file '+SWAP_PATH+'/input_iFeatures.txt --nlag 5 --out ./descriptors/'+TRAINING_SET+'/'+str(d)+'.txt')
        else:
            if(d=="CKSAAP" or d=="CKSAAGP"):
                os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures.txt 4 ./descriptors/'+TRAINING_SET+'/'+str(d)+'.txt')
            else:
                if(d=="PAAC" or d=="APAAC" or d=="SOCNumber" or d=="QSOrder"):
                    os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures.txt 5 ./descriptors/'+TRAINING_SET+'/'+str(d)+'.txt')
                    
                    
                else:
                    os.system('python ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_iFeatures.txt --type '+str(d)+' --out ./descriptors/'+TRAINING_SET+'/'+str(d)+'.txt')
                    print('python ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_iFeatures.txt --type '+str(d)+' --out ./descriptors/'+TRAINING_SET+'/'+str(d)+'.txt')        

print("Done!")


 
