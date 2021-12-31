# This script merge together all the descriptors extracted via iFeature
import os

SEQ_DATA = {}
DESCRIPTORS_ORDER = []

TOTAL_Y = 0
TOTAL_N = 0

#Reading TARGET output
with open("./BALANCED_1032_LEN6_INPUT_SEQUENCES.csv") as reader:
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
                    
print("Y:" + str(TOTAL_Y))
print("N:" + str(TOTAL_N))


#Write the header of the complete output
print("Writing Header...")
with open("./classificator_input_balanced_len6_1032seqs.txt","w") as writer:
    writer.write("SEQUENCE\t")

    # Merge the headers for the descriptors that allows different length sequenceing
    descr = ["QSOrder","SOCNumber","APAAC","PAAC","CKSAAGP","CKSAAP","NMBroto","Geary","Moran","BINARY","EAAC","AAINDEX","ZSCALE","BLOSUM62","EGAAC","AAC","DPC","DDE","TPC","GAAC","GDPC","GTPC","CTDC","CTDT","CTDD","CTriad","KSCTriad"]    
    for d in descr:
        print("Merging descriptors " + str(d))
        #open descriptor data, then append the descriptor columns
        with open("./descriptors/BALANCED_1032_LEN6_INPUT_SEQUENCES/"+str(d)+".txt") as reader:
            head = reader.readline()
            head = head.replace("\n","")
            hData = head.split("\t")                        
            hData= hData[1:]
            #append the descriptors
            for h in hData:
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
                    print("Incoerence detected:" + str(SEQ) + " not found in dictionary")
                    SEQ_DATA[SEQ]={}
                    exit()
                #for each descriptor in hData fill the dictionary of the current
                #sequence
                sData = sData[1:]                
                for i in range(0,len(hData)):
                    SEQ_DATA[SEQ][hData[i]]=sData[i]                           
            #go to the next descriptors file
    writer.write("TARGET\n")
    #write the output
    for SEQ in SEQ_DATA:
        writer.write(str(SEQ)+"\t")
        for d in DESCRIPTORS_ORDER:
            writer.write(SEQ_DATA[SEQ][d])
            writer.write("\t")
        writer.write(SEQ_DATA[SEQ]["TARGET"])
        writer.write("\n")

print("There are " + str(len(DESCRIPTORS_ORDER))+ " descriptors available!")
print(DESCRIPTORS_ORDER)











