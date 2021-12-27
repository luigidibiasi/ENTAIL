# This script executes iFeatures for the training dataset
import os


#build iFeature input
with open("./input_iFeatures.txt","w") as writer:
    with open("./input_sequences.csv") as reader:
        reader.readline()
        for l in reader:
            lData = l.split("\t")
            seq = lData[0]
            writer.write(">"+str(seq)+"\n")
            writer.write(str(seq)+"\n")

#Extract descriptor that allows different length
descr = ["AAC","DPC","DDE","TPC","GAAC","GDPC","GTPC","CTDC","CTDT","CTDD","CTriad","KSCTriad"]
for d in descr:
    b = os.path.getsize("./descriptors/"+str(d)+".txt")
    if (b<=30):
        print("Executing " + d);
        os.system('python ../iFeature/iFeature.py --file ./input_iFeatures.txt --type '+str(d)+' --out ./descriptors/'+str(d)+'.txt')

descr = ["BINARY","EAAC","AAINDEX","ZSCALE","BLOSUM62","EGAAC"]
with open("./input_sequences.csv") as reader:
    reader.readline()
    for l in reader:
        for d in descr:
            lData = l.split("\t")
            seq = lData[0]
            print("iFeature on " + seq)
            with open("./input_iFeatures_single.txt","w") as writer:
                writer.write(">"+str(seq)+"\n")
                writer.write(str(seq)+"\n")
                writer.close()
            print('python ../iFeature/iFeature.py --file ./input_iFeatures_single.txt --type '+str(d)+' --out ./descriptors/single/'+seq+'_'+str(d)+'.txt')
            os.system('python ../iFeature/iFeature.py --file ./input_iFeatures_single.txt --type '+str(d)+' --out ./descriptors/single/'+seq+'_'+str(d)+'.txt')
            
            
            

#"KNNprotein" how to use?
#"KNNpeptide"
#SSEC
#"TA"
#"ASA"
#"CKSAAP","CKSAAGP"            
#"NMBroto"
#"Moran"
#,"Geary"
#"SOCNumber","QSOrder"
#"PAAC","APAAC"
#"PSSM"
#SSEC
            #SSEB
#"Disorder","DisorderC","DisorderB"           
#,,"SSEC","SSEB",
