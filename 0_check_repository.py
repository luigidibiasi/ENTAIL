# This script check the repository integrity
# to made reproducible this work on different machine

import os
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


#Check Predicted Structures (PDB)
sequences = {}
with open(WALTZDB_PATH) as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[1]

with open(AMYLOAD_PATH) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split(",")
        SEQ_KEY = dLine[3]
        SEQ_KEY = SEQ_KEY.replace("\"","")        
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[4]
        
        

print("\tTotal sequences: " + str(len(sequences)))
print("\tChecking Structures...")
MISSING_PDB = 0
for seq in sequences:
    PDB_STATUS = "[FOUND]"
    if (not os.path.isfile(STRUCTURES_PATH+"/"+seq+".pdb")):
        MISSING_PDB+=1
        PDB_STATUS="[MISSING]"
        print(seq + " " + PDB_STATUS)

if (MISSING_PDB>0):
    print("\tIt is looks like that one or more PDB are missing. Please check the latest version of the repository.")
else:
    print("\tNo problems found")
