# This script takes the raw data from the Waltzdb and AmyLoad datasets
# and prepare:
#
# a) an unbalaced training (input_sequences.csv) set composed by 1803 sequences  (merging together the Waltzdb and AmyLoad dataset)
# b) a balaced training set (BALANCED_1412_input_sequences.csv) composed by 1412 sequences (706 for each classes)
# c) a balaced training set (BALANCED_706_input_sequences) composed by 706 sequences (353 for each classess) and a balaced test set composed by 706 sequences
# d) an unbalaced training set (UNBALANCED_LEN6) composed by sequences of same length
# e) a balanced training set (UNBALANCED_LEN6) composed by sequences of same length

dataset = {}
with open("./waltzdb_export.csv") as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        if (not SEQ_KEY in dataset):
            dataset[SEQ_KEY] = dLine[1]
with open("./amyload_session_unlogged_unlogged.csv") as reader:
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
            
# a) an unbalaced training (input_sequences.csv) set composed by 1803 sequences  (merging together the Waltzdb and AmyLoad dataset)
with open("./input_sequences.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:
        is_amil = dataset[seq]
        if ("non-amyloid" in is_amil):
            is_amil="No";
            dataset[seq]=is_amil
        else:
            if("amyloid" in is_amil):
                is_amil="Yes";
                dataset[seq]=is_amil
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")


# b) a balaced training set (BALANCED_1412_input_sequences.csv) composed by 1412 sequences (706 for each classes)

WRITTEN_Y = 0
WRITTEN_N = 0
with open("./BALANCED_1412_input_sequences.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:
        is_amil = dataset[seq]
        if (is_amil=="Yes"):
            if (WRITTEN_Y>=706):
                continue;            
            WRITTEN_Y+=1        
        if (is_amil=="No"):                    
            if (WRITTEN_N>=706):
                continue;            
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("BALACED 1412 DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")


# c) a balaced training set (BALANCED_706_input_sequences) composed by 706 sequences (353 for each classess) and a balaced test set composed by 706 sequences
test_dataset= {}
WRITTEN_Y = 0
WRITTEN_N = 0
with open("./BALANCED_706_input_sequences.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:
        is_amil = dataset[seq]
        if (is_amil=="Yes"):
            if (WRITTEN_Y>=353):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_Y+=1        
        if (is_amil=="No"):                    
            if (WRITTEN_N>=353):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("BALACED 706 DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")
AMIL_Y=0
AMIL_N=0
for seq in test_dataset:
    is_amil = dataset[seq]
    if (is_amil=="Yes"):
        AMIL_Y+=1
    if (is_amil=="No"):
        AMIL_N+=1        

WRITTEN_Y = 0
WRITTEN_N = 0
with open("./TESTSET_706_input_sequences.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:
        is_amil = dataset[seq]
        if (is_amil=="Yes"):
            if (WRITTEN_Y>=353):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_Y+=1        
        if (is_amil=="No"):                    
            if (WRITTEN_N>=353):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("TESTSET 706 DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")


# d) an unbalaced training set (UNBALANCED_LEN6) composed by sequences of same length
WRITTEN_Y = 0
WRITTEN_N = 0
with open("./UNBALANCED_LEN6_INPUT_SEQUENCES.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:
        is_amil = dataset[seq]
        if (is_amil=="Yes"):        
            WRITTEN_Y+=1        
        if (is_amil=="No"):                                
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("UNBALANCED_LEN6_INPUT_SEQUENCES  DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")

# e) a balanced training set (UNBALANCED_LEN6) composed by sequences of same length
test_dataset = {}
WRITTEN_Y = 0
WRITTEN_N = 0
with open("./BALANCED_1032_LEN6_INPUT_SEQUENCES.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:
        if (not len(seq)==6):            
            continue
        is_amil = dataset[seq]
        if (is_amil=="Yes"):
            if (WRITTEN_Y>=516):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_Y+=1        
        if (is_amil=="No"):                    
            if (WRITTEN_N>=516):
                test_dataset[seq]=is_amil
                continue;            
            WRITTEN_N+=1        
        seq = seq.replace("\"","")            
        writer.write(seq+"\t"+is_amil+"\n")
print("BALANCED_706_LEN6_INPUT_SEQUENCES  DONE. Written " + str(WRITTEN_Y) + "=> Y, " + str(WRITTEN_N) + " => N")