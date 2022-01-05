# This script check the repository integrity
# to made reproducible this work on different machine

import os
import shutil
from src.common import *

print("Checking integrity...")



#Check AMYLOAD
if (not os.path.isfile(WALTZDB_PATH)):
    print("\tWALTZDB [Not Found].")
    exit()
else:
    print("\tWALTZDB [OK]")

#Check AMYLOAD
if (not os.path.isfile(AMYLOAD_PATH)):
    print("\tAMYLOAD [Not Found].")
else:
    print("\tAMYLOAD [OK]")

#Check Pep424
if (not os.path.isfile(PEP424_PATH)):
    print("\tPEP424 [Not Found].")
else:
    print("\tPEP424 [OK]")

#Check Pep424
if (not os.path.isfile(AMYPRO_PATH)):
    print("\tAMYPRO [Not Found].")
else:
    print("\tAMYPRO [OK]")



#Check Predicted Structures (PDB)
sequences = {}
sequences_data = {}
COLLISIONS = 0
TOTAL_Y=0
TOTAL_N =0
with open(WALTZDB_PATH) as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")
        IS_AMIL = dLine[1]
        IS_AMIL = IS_AMIL.lower()
        IS_AMIL = IS_AMIL.replace(" ","")
        if ("non-amyloid" in IS_AMIL):
            IS_AMIL = "No"
        else:                
            if ("amyloid" in IS_AMIL):
                IS_AMIL="Yes"
            else:
                print("Dataset WALTZDB is invalid.")
                print("Please check the following line:")
                print(line)
                exit()
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = IS_AMIL
            sequences_data[SEQ_KEY] = {}
            sequences_data[SEQ_KEY]['IsAmil'] = IS_AMIL
            sequences_data[SEQ_KEY]['source'] = []
            sequences_data[SEQ_KEY]['source'].append('waltz-db')
        else:
            COLLISIONS+=1

with open(AMYLOAD_PATH) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[3]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")
        IS_AMIL = dLine[4]
        IS_AMIL = IS_AMIL.lower()
        IS_AMIL = IS_AMIL.replace(" ","")
        #Yes, we know that this check is redundant. No worry.
        if ("no" in IS_AMIL):
            IS_AMIL = "No"
        else:                
            if ("yes" in IS_AMIL):
                IS_AMIL="Yes"
            else:
                print("Dataset AMYLOAD is invalid.")
                print("Please check the following line:")
                print(line)
                exit()        
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[4]
            sequences_data[SEQ_KEY] = {}
            sequences_data[SEQ_KEY]['IsAmil'] = IS_AMIL
            sequences_data[SEQ_KEY]['source'] = []
            sequences_data[SEQ_KEY]['source'].append('amyload-db')
        else:
            sequences_data[SEQ_KEY]['source'].append('amyload-db')
            COLLISIONS+=1            

with open(PEP424_PATH) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[1]        
        SEQ_KEY = SEQ_KEY.replace("\"","")
        SEQ_KEY = SEQ_KEY.replace(" ","")
        IS_AMIL = dLine[2]
        IS_AMIL = IS_AMIL.lower()
        IS_AMIL = IS_AMIL.replace(" ","")
        #Yes, we know that this check is redundant. No worry.
        if ("-" in IS_AMIL):
            IS_AMIL = "No"
        else:                
            if ("+" in IS_AMIL):
                IS_AMIL="Yes"
            else:
                print("Dataset PEP24 is invalid.")
                print("Please check the following line:")
                print(line)
                exit()             
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = IS_AMIL
            sequences_data[SEQ_KEY] = {}
            sequences_data[SEQ_KEY]['IsAmil'] = IS_AMIL
            sequences_data[SEQ_KEY]['source'] = []
            sequences_data[SEQ_KEY]['source'].append('amyload-db')
        else:
            COLLISIONS+=1
            sequences_data[SEQ_KEY]['source'].append('pep424-db')
print("COLLISION DETECTED: " + str(COLLISIONS))

#parse AMYPRO database
AMYPRO_SIZE = 0
AMYPRO_LEN_6 = 0
with open(AMYPRO_PATH) as reader:    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")        
        CATEGORY = dLine[7]
        SEQ_KEY = dLine[11]
        if (not "amyloid" in CATEGORY):
            continue        
        AMYPRO_SIZE+=1
        
        if (SEQ_KEY=="-"):
            sData = dLine[12].split(",")            
        else:
            sData = SEQ_KEY.split(",")
            
        for SEQ_KEY in sData:
            if (len(SEQ_KEY)==6):
                AMYPRO_LEN_6+=1
            if (not SEQ_KEY in sequences):
                sequences[SEQ_KEY] = "Yes"
                sequences_data[SEQ_KEY] = {}
                sequences_data[SEQ_KEY]['IsAmil'] = "Yes"
                sequences_data[SEQ_KEY]['source'] = []
                sequences_data[SEQ_KEY]['source'].append('amypro-db')
            else:
                sequences_data[SEQ_KEY]['source'].append('amypro-db')
                print(SEQ_KEY)
                COLLISIONS+=1     
print("AMYPRO amyloid detected: " + str(AMYPRO_SIZE))
print("COLLISION DETECTED: " + str(COLLISIONS))
print("AMYPRO LEN 6 DETECTED: " + str(AMYPRO_LEN_6))


# Check dataset balancing status

for seq in sequences:
    if (sequences[seq]=="No"):
        TOTAL_N+=1
    else:
        if (sequences[seq]=="Yes"):
            TOTAL_Y+=1
        else:
            print("Invalid data in sequences list")
            print("This message might indicate a bug. Please contact ldibiasi@unisa.it")            
            exit()
            
print("\tTotal sequences: " + str(len(sequences)))
print("\tTotal AMYLOYD: " + str(TOTAL_Y))
print("\tTotal NON-AMYLOYD: " + str(TOTAL_N))

# Check dataset balancing status for sequence with len 6
TOTAL_Y=0
TOTAL_N =0
for seq in sequences:
    if (not len(seq)==6):
        continue;
    if (sequences[seq]=="No"):
        TOTAL_N+=1
    else:
        if (sequences[seq]=="Yes"):
            TOTAL_Y+=1
        else:
            print("Invalid data in sequences list")
            print("This message might indicate a bug. Please contact ldibiasi@unisa.it")            
            exit()

print("\t\tTotal (Len6) AMYLOYD: " + str(TOTAL_Y))
print("\t\tTotal (Len6) NON-AMYLOYD: " + str(TOTAL_N))

print("\tTotal collision (dataset overlapping): " + str(COLLISIONS))    
print("\tChecking Structures...")
MISSING_PDB = 0
for seq in sequences:
    PDB_STATUS = "[FOUND]"
    if (not os.path.isfile(STRUCTURES_PATH+"/"+seq+".pdb")):
        MISSING_PDB+=1
        PDB_STATUS="[MISSING]"
        print(seq + " " + PDB_STATUS)

#detect length classess
LEN_CLASSES = {}
for seq in sequences:
    slen = len(seq)    
    if (not slen in LEN_CLASSES):
        LEN_CLASSES[slen]=[]
    LEN_CLASSES[slen].append(seq)

print("\tSequences length classes:")
for c in LEN_CLASSES:
    print("\t\t"+str(c)+"=>"+str(len(LEN_CLASSES[c])))

if (MISSING_PDB>0):
    print("\tIt is looks like that one or more PDB are missing. Please check the latest version of the repository.")
    print("\tScript execution was aborted.")
    #exit()
else:
    print("\tNo problems found")


#Build SySa input
for seq in sequences:
    if (not len(seq)==6):
        continue
    with open("./classificator_inputs/SySa_Input/"+sequences[seq]+"_"+seq+".txt","w") as writer:
        writer.write(seq)
        writer.close()


# Generate Training and Test set. Please refer to README if you need more information regarding 'validation'

TRAINING_SET = SWAP_PATH+"/TrainingSet_2.csv";
TEST_SET = SWAP_PATH+"/TestSet_2.csv"


print("\n")
print("#################################")
print("# GENERATING TRAINING DATASET   #")
print("#################################")
to_testset={}
WRITTEN_Y=0
WRITTEN_N =0
with open(TRAINING_SET,"w") as writer:
    writer.write("SEQUENCE\tIS_AMYL\n")
    for seq in sequences:
        if (not len(seq)==6):
            continue;
        if (sequences[seq]=="No"):
            if (WRITTEN_N>=TRAININGSET_SIZE/2):
                to_testset[seq]=sequences[seq]
                continue;
        if (sequences[seq]=="Yes"):
            if (WRITTEN_Y>=TRAININGSET_SIZE/2):
                to_testset[seq]=sequences[seq]
                continue;    
        writer.write(seq)
        writer.write("\t")
        writer.write(sequences[seq])
        writer.write("\n")
        if (sequences[seq]=="No"):
            WRITTEN_N+=1
        if (sequences[seq]=="Yes"):
            WRITTEN_Y+=1
print("\tWritten (Len6) AMYLOYD: " + str(WRITTEN_Y))
print("\tWritten (Len6) NON-AMYLOYD: " + str(WRITTEN_N))

print("\n")
print("#################################")
print("# GENERATING     TEST DATASET   #")
print("#################################")

WRITTEN_Y=0
WRITTEN_N =0
with open(TEST_SET,"w") as writer:
    writer.write("SEQUENCE\tIS_AMYL\n")
    for seq in to_testset:
        if (not len(seq)==6):
            continue;
        if (sequences[seq]=="No"):
            if (WRITTEN_N>=TESTSET_SIZE/2):
                to_testset[seq]=sequences[seq]
                continue;
        if (sequences[seq]=="Yes"):
            if (WRITTEN_Y>=TESTSET_SIZE/2):
                to_testset[seq]=sequences[seq]
                continue;    
        writer.write(seq)
        writer.write("\t")
        writer.write(sequences[seq])
        writer.write("\n")
        if (sequences[seq]=="No"):
            WRITTEN_N+=1
        if (sequences[seq]=="Yes"):
            WRITTEN_Y+=1
print("\tWritten (Len6) AMYLOYD: " + str(WRITTEN_Y))
print("\tWritten (Len6) NON-AMYLOYD: " + str(WRITTEN_N))


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
            seq = lData[0]
            writer.write(">"+str(seq)+"\n")
            writer.write(str(seq)+"\n")

with open(SWAP_PATH +"/input_iFeatures_TestSet.txt","w") as writer:
    with open(TEST_SET) as reader:
        reader.readline()
        for l in reader:
            lData = l.split("\t")
            seq = lData[0]
            writer.write(">"+str(seq)+"\n")
            writer.write(str(seq)+"\n")




descr = DESCRIPTORS_TOUSE
for d in descr:    
    b=0
    if (b<=30):
        print("\tComputing " + d);
        if (d=="Moran" or d=="Geary" or d=="NMBroto"):
            os.system('python ./iFeature/codes/'+d+'.py --file '+SWAP_PATH+'/input_iFeatures.txt --nlag 5 --out '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
            os.system('python ./iFeature/codes/'+d+'.py --file '+SWAP_PATH+'/input_iFeatures_TestSet.txt --nlag 5 --out '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
        else:
            if(d=="CKSAAP" or d=="CKSAAGP"):
                os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures.txt 4 '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures_TestSet.txt 4 '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
            else:
                if(d=="PAAC" or d=="APAAC" or d=="SOCNumber" or d=="QSOrder"):
                    os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures.txt 5  '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                    os.system('python ./iFeature/codes/'+d+'.py '+SWAP_PATH+'/input_iFeatures_TestSet.txt 5  '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')                                    
                else:
                    os.system('python ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_iFeatures.txt --type '+str(d)+' --out '+TRAINING_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                    os.system('python ./iFeature/iFeature.py --file '+SWAP_PATH+'/input_iFeatures_TestSet.txt --type '+str(d)+' --out '+TEST_DESCRIPTORS_PATH+'/'+str(d)+'.txt')
                    




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
