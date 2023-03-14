# This script check the repository integrity
# to made reproducible this work on different machine

import os
import shutil
from src.common import *
import textwrap

print("Checking integrity...")



#Check SNARE
if (not os.path.isfile(SNARE_PATH)):
    print("\tSNARE [Not Found].")
    exit()
else:
    print("\tSNARE [OK]")

#Check NONSNARE
if (not os.path.isfile(NONSNARE_PATH)):
    print("\tNONSNARE [Not Found].")
else:
    print("\tNONSNARE [OK]")

sequences = {}
TOTAL_N=0
TOTAL_Y=0

with open(SNARE_PATH) as reader:
	CUR_SEQ = ""
	SEQ_BODY=""
	LAST_SEQ = None
	for line in reader:
		line = line.replace("\n","").replace("\r","")
		if (">" in line):
			CUR_SEQ = line.split("|")[1]
			print(CUR_SEQ)
			if (CUR_SEQ!=LAST_SEQ and LAST_SEQ!=None):
				sequences[LAST_SEQ]={}
				sequences[LAST_SEQ]['BODY'] = SEQ_BODY;
				sequences[LAST_SEQ]['IS_SNARE']="Yes";
				SEQ_BODY=""
			LAST_SEQ=CUR_SEQ
			continue;
		SEQ_BODY = SEQ_BODY + line		
	sequences[LAST_SEQ]={}
	sequences[LAST_SEQ]['BODY'] = SEQ_BODY;
	sequences[LAST_SEQ]['IS_SNARE']="Yes";

with open(NONSNARE_PATH) as reader:
	CUR_SEQ = ""
	SEQ_BODY=""
	LAST_SEQ = None
	for line in reader:
		line = line.replace("\n","").replace("\r","")
		if (">" in line):
			CUR_SEQ = line.split("|")[0].split(":")[0].replace(">","")
			print(CUR_SEQ)
			if (CUR_SEQ!=LAST_SEQ and LAST_SEQ!=None):
				sequences[LAST_SEQ]={}
				sequences[LAST_SEQ]['BODY'] = SEQ_BODY;
				sequences[LAST_SEQ]['IS_SNARE']="No";
				SEQ_BODY=""
			LAST_SEQ=CUR_SEQ
			continue;
		SEQ_BODY = SEQ_BODY + line		
	sequences[LAST_SEQ]={}
	sequences[LAST_SEQ]['BODY'] = SEQ_BODY;
	sequences[LAST_SEQ]['IS_SNARE']="No";


print(sequences["2XU5"])





# Check dataset balancing status
for seq in sequences:
    if (sequences[seq]['IS_SNARE']=="No"):
        TOTAL_N+=1
    else:
        if (sequences[seq]['IS_SNARE']=="Yes"):
            TOTAL_Y+=1
        else:
            print("Invalid data in sequences list")
            print("This message might indicate a bug. Please contact ldibiasi@unisa.it")            
            exit()
            
print("\tTotal sequences: " + str(len(sequences)))
print("\tTotal SNARE " + str(TOTAL_Y))
print("\tTotal NON-SNARE: " + str(TOTAL_N))

#detect length classess
LEN_CLASSES = {}
for seq in sequences:
    slen = len(sequences[seq]['BODY'])    
    if (not slen in LEN_CLASSES):
        LEN_CLASSES[slen]=[]
    LEN_CLASSES[slen].append(seq)

print("\tSequences length classes:")
for c in LEN_CLASSES:
    print("\t\t"+str(c)+"=>"+str(len(LEN_CLASSES[c])))

#Build SySa input
for seq in sequences:
    print(seq)
    seq_name = seq
    seq_body = sequences[seq]['BODY']
    seq_snare = sequences[seq]['IS_SNARE'];
    with open("./classificator_inputs/SySa_Input/"+seq_name+"_"+seq_snare+".txt","w") as writer:
        writer.write(seq_body)
        writer.close()

# Generate Training and Test set. Please refer to README if you need more information regarding 'validation'

TRAINING_SET = SWAP_PATH+"/TrainingSet_SNARER2.csv";
TEST_SET = SWAP_PATH+"/TestSet_SNARER2.csv"


print("\n")
print("#################################")
print("# GENERATING TRAINING DATASET   #")
print("#################################")
to_testset={}
WRITTEN_Y=0
WRITTEN_N =0
with open(TRAINING_SET,"w") as writer:
    writer.write("SEQUENCE\tIS_SNARE\n")
    for seq in sequences:
        if (sequences[seq]['IS_SNARE']=="No"):
            if (WRITTEN_N>=TRAININGSET_SIZE/2):
                to_testset[seq]['BODY']=sequences[seq]['BODY']
                continue;
        if (sequences[seq]['IS_SNARE']=="Yes"):
            if (WRITTEN_Y>=TRAININGSET_SIZE/2):
                to_testset[seq]['BODY']=sequences[seq]['BODY']
                continue;    
        writer.write(seq)
        writer.write("\t")
        writer.write(sequences[seq]['IS_SNARE'])
        writer.write("\t")
        writer.write(sequences[seq]['BODY'])
        writer.write("\n")
        
print("\n")
print("#################################")
print("# GENERATING     TEST DATASET   #")
print("#################################")

WRITTEN_Y=0
WRITTEN_N =0
with open(TEST_SET,"w") as writer:
    writer.write("SEQUENCE\tIS_SNARE\n")
    for seq in to_testset:
        if (sequences[seq]['IS_SNARE']=="No"):
            if (WRITTEN_N>=TESTSET_SIZE/2):
                to_testset[seq]['BODY']=sequences[seq]['BODY']
                continue;
        if (sequences[seq]['IS_SNARE']=="Yes"):
            if (WRITTEN_Y>=TESTSET_SIZE/2):
                to_testset[seq]['BODY']=sequences[seq]['BODY']
                continue;    
        writer.write(seq)
        writer.write("\t")
        writer.write(sequences[seq]['IS_SNARE'])
        writer.write("\t")
        writer.write(sequences[seq]['BODY'])
        writer.write("\n")


print("\n")
print("#################################")
print("# CHECK DATASETS  INTEGRITY     #")
print("#################################")


sequences = {}
with open(TRAINING_SET) as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")        
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[1]

with open(TEST_SET) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")        
        if (SEQ_KEY in sequences):
            print("TEST SET IS INVALID")
            print("The sequence " + SEQ_KEY + " is still in training set")
            exit()

sequences = {}
with open(TEST_SET) as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")                
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[1]

with open(TRAINING_SET) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")        
        if (SEQ_KEY in sequences):
            print("TEST SET IS INVALID")
            print("The sequence " + SEQ_KEY + " is still in training set")
            exit()

print("\tTRAINING and TESt set are OK.")
print("\tNo common sequences detected")

        
#Extract descriptor that allows different length
print("####################################")
print("# COMPUTING MOLECULAR DESCRIPTORS  #")
print("####################################")

        
#build iFeature input
print("Preparing iFeature input...")
with open(SWAP_PATH +"/input_iFeatures.txt","w") as writer:
    with open(TRAINING_SET) as reader:
        reader.readline()
        for l in reader:
            lData = l.split("\t")
            seq = lData[2].replace("\n","")
            writer.write(">"+str(lData[0])+"\n")
            chunks = textwrap.fill(seq, 80)
            writer.write(str(chunks)+"\n")
            break;

with open(SWAP_PATH +"/input_iFeatures_TestSet.txt","w") as writer:
    with open(TEST_SET) as reader:
        reader.readline()
        for l in reader:
            break
            lData = l.split("\t")
            seq = lData[2].replace("\n","")
            writer.write(">"+str(lData[0])+"\n")
            writer.write(str(seq)+"\n\n")
            break;



descr = DESCRIPTORS_TOUSE
for d in descr:    
    b=0
    if (b<=30):
        print("\tComputing " + d);
        if (d=="Moran" or d=="Geary" or d=="NMBroto"):
            os.system('python3.11 ./iFeature/codes/'+d+'.py --file '+SWAP_PATH+'/input_iFeatures.txt --nlag 5 --out '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
            os.system('python3.11 ./iFeature/codes/'+d+'.py --file '+SWAP_PATH+'/input_iFeatures_TestSet.txt --nlag 5 --out '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
        else:
            if(d=="CKSAAP" or d=="CKSAAGP"):
                os.system('python3.11 ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures.txt 4 '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                os.system('python3.11 ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures_TestSet.txt 4 '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
            else:
                if(d=="PAAC" or d=="APAAC" or d=="SOCNumber" or d=="QSOrder"):
                    os.system('python3.11 ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures.txt 10  '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                    os.system('python3.11 ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures_TestSet.txt 5  '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')                                    
                else:
                    os.system('python3.11 ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_iFeatures.txt --type '+str(d)+' --out '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                    os.system('python3.11 ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_iFeatures_TestSet.txt --type '+str(d)+' --out '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                    
exit()



#Extract descriptor that allows different length
print("####################################")
print("# FINALIZING CLASSIFICATOR INPUT  #")
print("####################################")


# Copy YPredStruct into TRAININGSET and TESTSET directory
# These descriptors were computed by YASARA
shutil.copyfile('./datasets/YPredStruct.txt',TRAINING_DESCRIPTORS_PATH+'/YPredStruct.txt')
shutil.copyfile('./datasets/YPredStruct.txt',TEST_DESCRIPTORS_PATH+'/YPredStruct.txt')


print("\tPreparing TRAININGSET:")
SEQ_DATA = {}
DESCRIPTORS_ORDER = []
TOTAL_Y = 0
TOTAL_N = 0
#Reading TARGET output
with open(TRAINING_SET) as reader:
    reader.readline()
    for SEQ in reader:
        SEQ = SEQ.replace("\n","")
        sData = SEQ.split("\t")        
        if (not sData[0] in SEQ_DATA):
            SEQ_DATA[sData[0]]={}
            SEQ_DATA[sData[0]]["TARGET"]=sData[1]
            if (sData[1]=="Yes"):
                TOTAL_Y+=1
            else:
                if (sData[1]=="No"):
                    TOTAL_N+=1                
print("\t\tDetected AMYLOID:" + str(TOTAL_Y))
print("\t\tDetected NOTAMYL:" + str(TOTAL_N))
    

#Write the header of the complete output
print("\t\tWriting Header...")
with open("./classificator_inputs/TrainingSet.txt","w") as writer:
    writer.write("SEQUENCE\t")
    # Merge the headers for the descriptors that allows different length sequenceing
    descr = DESCRIPTORS_TOUSE
    for d in descr:
        print("\t\tPushing descriptor " + str(d))
        #open descriptor data, then append the descriptor columns
        with open(TRAINING_DESCRIPTORS_PATH+"/"+str(d)+".txt") as reader:
            head = reader.readline()
            head = head.replace("\n","")
            hData = head.split("\t")                        
            hData= hData[1:]
            #append the descriptors
            for h in hData:
                if (not str(h) in DESCRIPTORS_ORDER):
                    writer.write(str(h)+"\t")
                    DESCRIPTORS_ORDER.append(str(h))

            #now read the file content and fill the SEQ_DATA dictionary
            for seq_data in reader:                
                seq_data = seq_data.replace("\n","")
                sData = seq_data.split("\t")
                SEQ = sData[0]
                if (SEQ=="SEQUENCE"):
                    continue;
                if (not SEQ in SEQ_DATA):
                    if (d=="YPredStruct"):
                        continue
                    print("Incoerence detected:" + str(SEQ) + " not found in dictionary")
                    SEQ_DATA[SEQ]={}
                    exit()
                #for each descriptor in hData fill the dictionary of the current
                #sequence
                sData = sData[1:]                
                for i in range(0,len(hData)):
                    SEQ_DATA[SEQ][hData[i]]=sData[i]                           
            #go to the next descriptors file
    writer.write("TARGET\tSOURCE\n")
    #write the output
    for SEQ in SEQ_DATA:
        writer.write(str(SEQ)+"\t")
        for d in DESCRIPTORS_ORDER:
            writer.write(SEQ_DATA[SEQ][d])
            writer.write("\t")
        writer.write(SEQ_DATA[SEQ]["TARGET"])
        writer.write("\t")
        for s in sequences_data[SEQ]["source"]:
            writer.write(s+"|")
        writer.write("\n")


print("\tPreparing TESTSET:")
SEQ_DATA = {}
DESCRIPTORS_ORDER = []
TOTAL_Y = 0
TOTAL_N = 0
#Reading TARGET output
with open(TEST_SET) as reader:
    reader.readline()
    for SEQ in reader:
        SEQ = SEQ.replace("\n","")
        sData = SEQ.split("\t")        
        if (not sData[0] in SEQ_DATA):
            SEQ_DATA[sData[0]]={}
            SEQ_DATA[sData[0]]["TARGET"]=sData[1]
            if (sData[1]=="Yes"):
                TOTAL_Y+=1
            else:
                if (sData[1]=="No"):
                    TOTAL_N+=1                
print("\t\tDetected AMYLOID:" + str(TOTAL_Y))
print("\t\tDetected NOTAMYL:" + str(TOTAL_N))
    

#Write the header of the complete output
print("\tWriting Header...")
with open("./classificator_inputs/TestSet.txt","w") as writer:
    writer.write("SEQUENCE\t")
    # Merge the headers for the descriptors that allows different length sequenceing
    descr = DESCRIPTORS_TOUSE
    for d in descr:
        print("\t\tPushing descriptor " + str(d))
        #open descriptor data, then append the descriptor columns
        with open(TEST_DESCRIPTORS_PATH+"/"+str(d)+".txt") as reader:
            head = reader.readline()
            head = head.replace("\n","")
            hData = head.split("\t")                        
            hData= hData[1:]
            #append the descriptors
            for h in hData:
                if (not str(h) in DESCRIPTORS_ORDER):
                    writer.write(str(h)+"\t")
                    DESCRIPTORS_ORDER.append(str(h))

            #now read the file content and fill the SEQ_DATA dictionary
            for seq_data in reader:                
                seq_data = seq_data.replace("\n","")
                sData = seq_data.split("\t")
                SEQ = sData[0]
                if (SEQ=="SEQUENCE"):
                    continue;
                if (not SEQ in SEQ_DATA):
                    if (d=="YPredStruct"):
                        continue
                    print("Incoerence detected:" + str(SEQ) + " not found in dictionary")
                    SEQ_DATA[SEQ]={}
                    exit()
                #for each descriptor in hData fill the dictionary of the current
                #sequence
                sData = sData[1:]                
                for i in range(0,len(hData)):
                    SEQ_DATA[SEQ][hData[i]]=sData[i]                           
            #go to the next descriptors file
    writer.write("TARGET\tSOURCE\n")
    #write the output
    for SEQ in SEQ_DATA:
        writer.write(str(SEQ)+"\t")
        for d in DESCRIPTORS_ORDER:
            writer.write(SEQ_DATA[SEQ][d])
            writer.write("\t")
        writer.write(SEQ_DATA[SEQ]["TARGET"])
        writer.write("\t")
        for s in sequences_data[SEQ]["source"]:
            writer.write(s+"|")
        writer.write("\n")

#Generate output for YAMIRA website (csv)
with open("./classificator_inputs/TrainingSet.txt") as reader:
    HEAD = reader.readline()
    with open("./classificator_inputs/CompleteSet.txt","w") as writer:
        writer.write(HEAD)
        for l in reader:
            writer.write(l)
        writer.close()
    reader.close()
with open("./classificator_inputs/TestSet.txt") as reader:
    reader.readline() # skip header
    with open("./classificator_inputs/CompleteSet.txt","a") as writer:        
        for l in reader:
            writer.write(l)
        writer.close()
    reader.close()

    
#MOVE THIS at the end of the script
#Generate output for YAMIRA website (csv)
with open("./classificator_inputs/TrainingSet.txt") as reader:
    reader.readline()
    with open("./classificator_inputs/OnlySequences.txt","w") as writer:
        writer.write("SEQUENCE\tSOURCES\n")
        for l in reader:            
            lData = l.split("\t")
            is_amil = lData[4046];
            if(is_amil=="No"):
                continue;
            writer.write(lData[0])
            writer.write("\t")
            for s in sequences_data[l.split("\t")[0]]['source']:
                writer.write(s+"|")
            writer.write("\n")
        writer.close()
    reader.close()
with open("./classificator_inputs/TestSet.txt") as reader:
    reader.readline() # skipheader
    with open("./classificator_inputs/OnlySequences.txt","a") as writer:        
        for l in reader:
            writer.write(l.split("\t")[0])
            writer.write("\t")
            for s in sequences_data[l.split("\t")[0]]['source']:
                writer.write(s+"|")
            writer.write("\n")
        writer.close()
    reader.close()



print("\n\nAll Done!")
print("The training and test sets are available into classificator_inputs directory.")
