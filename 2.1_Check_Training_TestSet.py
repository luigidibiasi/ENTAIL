# This script check the repository integrity
# to made reproducible this work on different machine

import os
from src.common import *

print("Checking integrity...")

TRAINING_SET = TRAINING_PATH+"/BALANCED_632_LEN6_3DSTRUCT.csv"
TEST_SET = TRAINING_PATH+"/TESTSET_BALANCED_400_input_sequences.csv"

sequences = {}
with open(TRAINING_SET) as reader:
    # skip header
    header = reader.readline()    
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[1]

with open(TEST_SET) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")        
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
        if (not SEQ_KEY in sequences):
            sequences[SEQ_KEY] = dLine[1]

with open(TRAINING_SET) as reader:
    for line in reader:        
        line = line.replace("\n","").replace("\r","")
        dLine = line.split("\t")
        SEQ_KEY = dLine[0]
        SEQ_KEY = SEQ_KEY.replace("\"","")        
        if (SEQ_KEY in sequences):
            print("TEST SET IS INVALID")
            print("The sequence " + SEQ_KEY + " is still in training set")
            exit()

print("Training and test set are OK. No common sequences detected")
        
        
