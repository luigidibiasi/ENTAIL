# This script execute prediction on new data 

import os
import shutil
import sys
from src.common import *

if (len(sys.argv)!=3):    
    print("Please use predict.py <MODEL_ID> <SEQUENCE>")
    exit()

MODEL = sys.argv[1]
SEQ = sys.argv[2]

if (len(SEQ)!=6):
    print("SEQUENCE length must be 6")
    exit()

PREDICTION_DESCRIPTORS_PATH = "./swap/prediction/"
isExist = os.path.exists(PREDICTION_DESCRIPTORS_PATH)
if (not isExist):
      os.makedirs(PREDICTION_DESCRIPTORS_PATH)
PREDICTION_DESCRIPTORS_PATH = "./swap/prediction/"+SEQ;
isExist = os.path.exists(PREDICTION_DESCRIPTORS_PATH)
if (not isExist):
      os.makedirs(PREDICTION_DESCRIPTORS_PATH)
      
print("Setting up prediction with:")
print("\tMODEL: " + str(MODEL))
print("\tSEQUENCE: "+SEQ)
print("\tOUTPUT PATH: "+PREDICTION_DESCRIPTORS_PATH)

# Generate Input for iFeature
print("####################################")
print("# COMPUTING MOLECULAR DESCRIPTORS  #")
print("####################################")
        
#build iFeature input
print("Preparing iFeature input...")
with open(SWAP_PATH +"/input_predict.txt","w") as writer:
    writer.write(">"+str(SEQ)+"\n")
    writer.write(str(SEQ)+"\n")


descr = DESCRIPTORS_TOUSE
for d in descr:    
    b=0
    if (b<=30):
        print("\tComputing " + d);
        if (d=="Moran" or d=="Geary" or d=="NMBroto"):
            os.system('python ./iFeature/codes/'+d+'.py --file '+SWAP_PATH+'/input_predict.txt --nlag 5 --out '+PREDICTION_DESCRIPTORS_PATH+'/'+str(d)+'.txt')            
        else:
            if(d=="CKSAAP" or d=="CKSAAGP"):
                os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_predict.txt 4 '+PREDICTION_DESCRIPTORS_PATH+'/'+str(d)+'.txt')                
            else:
                if(d=="PAAC" or d=="APAAC" or d=="SOCNumber" or d=="QSOrder"):
                    os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_predict.txt 5  '+PREDICTION_DESCRIPTORS_PATH+'/'+str(d)+'.txt')                    
                else:
                    os.system('python ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_predict.txt --type '+str(d)+' --out '+PREDICTION_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                   
            



#Extract descriptor that allows different length
print("####################################")
print("# FINALIZING CLASSIFICATOR INPUT  #")
print("####################################")


# Copy YPredStruct into TRAININGSET and TESTSET directory
# These descriptors were computed by YASARA
shutil.copyfile('./datasets/YPredStruct.txt',PREDICTION_DESCRIPTORS_PATH+'/YPredStruct.txt')    

#Write the header of the complete output
DESCRIPTORS_ORDER = []
SEQ_DATA = {}
print("\t\tWriting Header...")
with open("./models/ENTAIL_3b/input.txt","w") as writer:
    writer.write("SEQUENCE")
    # Merge the headers for the descriptors that allows different length sequenceing
    descr = DESCRIPTORS_TOUSE
    for d in descr:
        print("\t\tPushing descriptor " + str(d))
        #open descriptor data, then append the descriptor columns
        with open(PREDICTION_DESCRIPTORS_PATH+"/"+str(d)+".txt") as reader:
            head = reader.readline()
            head = head.replace("\n","")
            hData = head.split("\t")                        
            hData= hData[1:]
            #append the descriptors
            for h in hData:
                if (not str(h) in DESCRIPTORS_ORDER):
                    writer.write("\t"+str(h))
                    DESCRIPTORS_ORDER.append(str(h))

            #now read the file content and fill the SEQ_DATA dictionary
            for seq_data in reader:                
                seq_data = seq_data.replace("\n","")
                sData = seq_data.split("\t")
                SEQ = sData[0]
                if (SEQ=="SEQUENCE"):
                    continue;
                if (not SEQ in SEQ_DATA):
                    SEQ_DATA[SEQ]={}
                    
                #for each descriptor in hData fill the dictionary of the current
                #sequence
                sData = sData[1:]                
                for i in range(0,len(hData)):
                    SEQ_DATA[SEQ][hData[i]]=sData[i]                           
            #go to the next descriptors file
    writer.write("\tTARGET\tSOURCE\n")
    #write the output
    for SEQ in SEQ_DATA:
        writer.write(str(SEQ))
        for d in DESCRIPTORS_ORDER:
            writer.write("\t")
            writer.write(SEQ_DATA[SEQ][d])            
        writer.write("\t?\t?")
        writer.write("\n")

print("Executing prediction...")
os.chdir('./models/ENTAIL_3b/')
os.system('entail_predict_e3.exe')            
