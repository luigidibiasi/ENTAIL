# This script takes the raw data from the Waltzdb and AmyLoad datasets
# and prepare:
#

# f) an input for YASARA macro (yasara_input.txt) composed by all the sequences (of length 6) for which we have a predicteed PDB structure
#
# Please note that the sequence STVIIR have no predicted structure. Then, it was removed from balaced dataset that uses YPredStruct descriptors
#
# Also, this script prepare the Pep242 dataset to be used as TEST set for ENTAIL




from src.common import *


dataset = {}
with open(WALTZDB_PATH) as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        if (not SEQ_KEY in dataset):
            dataset[SEQ_KEY] = dLine[1]
            
with open(AMYLOAD_PATH) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[3]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        if (not SEQ_KEY in dataset):
            dataset[SEQ_KEY] = dLine[4]

#detect length classess
LEN_CLASSES = {}
for seq in dataset:
    slen = len(seq)    
    if (not slen in LEN_CLASSES):
        LEN_CLASSES[slen]=[]
    LEN_CLASSES[slen].append(seq)

# Input dataset for YASARA macro
with open(SWAP_PATH+"/yasara_input.txt","w") as writer:    
    for seq in dataset:
        if (not len(seq)==6):
            continue;
        writer.write(seq+"\n")
    writer.close()




    

# g) a balanced training set (BALANCED_1030_LEN6_3DSTRUCT.csv) composed by sequences of same length
test_dataset = {}
WRITTEN_Y = 0
WRITTEN_N = 0
with open(TRAINING_PATH+"/BALANCED_632_LEN6.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:        
        if (not len(seq)==6):            
            continue
        if (seq=="STVIIR"):
            continue
        is_amil = dataset[seq]
        if (is_amil=="Yes"):
            if (WRITTEN_Y>=316):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_Y+=1        
        if (is_amil=="No"):                    
            if (WRITTEN_N>=316):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("BALANCED_632_LEN6_3DSTRUCT  DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")

# g) a balanced test set (BALANCED_400_LEN6_3DSTRUCT.csv) composed by sequences of same length
AMIL_Y=0
AMIL_N=0
for seq in test_dataset:
    is_amil = dataset[seq]
    if (is_amil=="Yes"):
        AMIL_Y+=1
    if (is_amil=="No"):
        AMIL_N+=1
print("Remaining " + str(AMIL_Y) + " " +str(AMIL_N))

WRITTEN_Y = 0
WRITTEN_N = 0
with open(TRAINING_PATH+"/TESTSET_BALANCED_400_LEN6.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in test_dataset:
        is_amil = test_dataset[seq]
        if (is_amil=="Yes"):
            if (WRITTEN_Y>=200):
                continue
            WRITTEN_Y+=1        
        if (is_amil=="No"):
            if (WRITTEN_N>=200):
                continue
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("TESTSET_BALANCED_400_LEN6  DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")

#Prepare PEP424 subset
#Extact only the sequence with len = 6
WRITTEN_Y = 0
WRITTEN_N = 0
with open(TRAINING_PATH+"/TESTSET_PEP424_LEN_6.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    with open(PEP424_PATH) as reader:
        # skip header
        header = reader.readline()    
        for line in reader:        
            line = line.replace("\n","").replace("\r","")
            dLine = line.split("\t")
            SEQ_KEY = dLine[1]
            SEQ_KEY = SEQ_KEY.replace("\"","")
            SEQ_KEY = SEQ_KEY.replace(" ","")
            if (not len(SEQ_KEY)==6):
                continue
            IS_AMIL = dLine[2]            
            IS_AMIL = IS_AMIL.replace("\n","")
            IS_AMIL = IS_AMIL.replace(" ","")
            if (IS_AMIL=="+"):
                IS_AMIL="Yes"
                WRITTEN_Y+=1
            if (IS_AMIL=="-"):
                IS_AMIL="No"
                WRITTEN_N+=1
            
            writer.write(SEQ_KEY+"\t"+IS_AMIL+"\n");
print("TESTSET_PEP424_LEN_6  DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")            

