# This script takes the raw data from the Waltzdb and AmyLoad datasets
# and transforms it into MATLAB ML/DL compatible input datasets.


dataset = {}

with open("./waltzdb_export.csv") as reader:
    # skip header
    header = reader.readline()
    print(header)
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
            

with open("./input_sequences.csv","w") as writer:
    writer.write("SEQUENCE\tIS_AMIL\n")
    for seq in dataset:

        is_amil = dataset[seq]
        if ("non-amyloid" in is_amil):
            is_amil="No";
        else:
            if("amyloid" in is_amil):
                is_amil="Yes";

        seq = seq.replace("\"","")
        
        
        writer.write(seq+"\t"+is_amil+"\n")
        
