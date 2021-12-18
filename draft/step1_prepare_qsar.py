
# Open Amminoacids descriptors table.
AMMINO = {}
r = open("./ammino_descriptors.txt");
r.readline() # skip first line (header)
while 1:
    row = r.readline()
    if (row==""):
        break;
    rdata = row.split("\t")
    AMMINO[rdata[0]] = {}
    AMMINO[rdata[0]]["ARGP820102"]=rdata[1];
    AMMINO[rdata[0]]["CHAM830101"]=rdata[2];
    AMMINO[rdata[0]]["CHAM830107"]=rdata[3];
    AMMINO[rdata[0]]["CHAM830108"]=rdata[4];
    AMMINO[rdata[0]]["CHOP780204"]=rdata[5];
    AMMINO[rdata[0]]["CHOP780205"]=rdata[6];
    AMMINO[rdata[0]]["CHOP780206"]=rdata[7];
    AMMINO[rdata[0]]["CHOP780207"]=rdata[8];
    AMMINO[rdata[0]]["EISD860101"]=rdata[9];
    AMMINO[rdata[0]]["FAUJ880108"]=rdata[10];
    AMMINO[rdata[0]]["FAUJ880111"]=rdata[11];
    AMMINO[rdata[0]]["FAUJ880112"]=rdata[12];
    AMMINO[rdata[0]]["GUYH850101"]=rdata[13];
    AMMINO[rdata[0]]["JANJ780101"]=rdata[14];
    AMMINO[rdata[0]]["KRIW790101"]=rdata[15];
    AMMINO[rdata[0]]["ZIMJ680102"]=rdata[16];
    AMMINO[rdata[0]]["ONEK900102"]=rdata[17];
    AMMINO[rdata[0]]["steric_parameter"]=rdata[18];
    AMMINO[rdata[0]]["polarizability"]=rdata[19];
    AMMINO[rdata[0]]["volume"]=rdata[20];
    AMMINO[rdata[0]]["isoelectric_point"]=rdata[21];
    AMMINO[rdata[0]]["helix_probability"]=rdata[22];
    AMMINO[rdata[0]]["sheet_probability"]=rdata[23];
    AMMINO[rdata[0]]["hydrophobicity"]=rdata[24];
r.close()

def WRITE_HEADER():
    entire = open("union.txt","w")
    entire.write("SEQ\tARGP820102\tCHAM830101\tCHAM830107\tCHAM830108\tCHOP780204\tCHOP780205\tCHOP780206\tCHOP780207\tEISD860101\tFAUJ880108\tFAUJ880111\tFAUJ880112\tGUYH850101\tJANJ780101\tKRIW790101\tZIMJ680102\tONEK900102\tSTERIC\tPOLAR\tVOL\tISOP\tHPROB\tSPROB\tHYDRO\tTARGET\n")
    entire.close()
    

WRITE_HEADER();
entire = open("union.txt","a")
with open("input_sequences.csv") as reader:
    # skip header
    reader.readline()
    for line in reader:
        line = line.replace("\n","")
        
        #extract sequence
        cprot = line.split("\t")[0]
        IS_AMIL = line.split("\t")[1]
        ARGP820102 = 0.0
        CHAM830101 = 0.0
        CHAM830107 = 0.0
        CHAM830108 = 0.0
        CHOP780204 = 0.0
        CHOP780205 = 0.0
        CHOP780206 = 0.0
        CHOP780207 = 0.0
        EISD860101 = 0.0
        FAUJ880108 = 0.0
        FAUJ880111 = 0.0
        FAUJ880112 = 0.0
        GUYH850101 = 0.0
        JANJ780101 = 0.0
        KRIW790101 = 0.0
        ZIMJ680102 = 0.0
        ONEK900102  = 0.0          
        steric_parameter = 0.0
        polarizability = 0.0
        volume = 0.0
        isoelectric_point = 0.0
        helix_probability = 0.0
        sheet_probability = 0.0
        hydrophobicity = 0.0
        
        for a in cprot:
            if (a=="X"):
                continue
            if (a=="U"):
                continue
            if (a=="m"):
                continue
            if (a=="-"):
                continue
            ARGP820102 += float(AMMINO[a]["ARGP820102"])
            CHAM830101 += float(AMMINO[a]["CHAM830101"])
            CHAM830107 += float(AMMINO[a]["CHAM830107"])
            CHAM830108 += float(AMMINO[a]["CHAM830108"])
            CHOP780204  += float(AMMINO[a]["CHOP780204"])
            CHOP780205  += float(AMMINO[a]["CHOP780205"])
            CHOP780206  += float(AMMINO[a]["CHOP780206"])
            CHOP780207  += float(AMMINO[a]["CHOP780207"])
            EISD860101  += float(AMMINO[a]["EISD860101"])
            FAUJ880108  += float(AMMINO[a]["FAUJ880108"])
            FAUJ880111  += float(AMMINO[a]["FAUJ880111"])
            FAUJ880112  += float(AMMINO[a]["FAUJ880112"])
            GUYH850101  += float(AMMINO[a]["GUYH850101"])
            JANJ780101  += float(AMMINO[a]["JANJ780101"])
            KRIW790101  += float(AMMINO[a]["KRIW790101"])
            ZIMJ680102  += float(AMMINO[a]["ZIMJ680102"])
            ONEK900102   += float(AMMINO[a]["ONEK900102"])
            steric_parameter += float(AMMINO[a]["steric_parameter"])
            polarizability += float(AMMINO[a]["polarizability"])
            volume  += float(AMMINO[a]["volume"])
            isoelectric_point  += float(AMMINO[a]["isoelectric_point"])                                            
            helix_probability  += float(AMMINO[a]["helix_probability"])                    
            sheet_probability  += float(AMMINO[a]["sheet_probability"])
            hydrophobicity  += float(AMMINO[a]["hydrophobicity"])
        ARGP820102 /= len(cprot)
        CHAM830101 /= len(cprot)
        CHAM830107 /= len(cprot)
        CHAM830108 /= len(cprot)
        CHOP780204 /= len(cprot)
        CHOP780205 /= len(cprot)
        CHOP780206 /= len(cprot)
        CHOP780207 /= len(cprot)
        EISD860101 /= len(cprot)
        FAUJ880108 /= len(cprot)
        FAUJ880111 /= len(cprot)
        FAUJ880112 /= len(cprot)
        GUYH850101 /= len(cprot)
        JANJ780101 /= len(cprot)
        KRIW790101 /= len(cprot)
        ZIMJ680102 /= len(cprot)
        ONEK900102 /= len(cprot)
        steric_parameter /= len(cprot)
        polarizability /= len(cprot)
        volume /= len(cprot)
        isoelectric_point /= len(cprot)
        helix_probability /= len(cprot)
        sheet_probability /= len(cprot)                
        hydrophobicity /= len(cprot)
        entire.write(cprot)
        entire.write(cprot+'\t'+str(ARGP820102)+'\t'+
        str(CHAM830101) + '\t' +
        str(CHAM830107) + '\t' +
        str(CHAM830108) + '\t' +
        str(CHOP780204) + '\t'+
        str(CHOP780205) + '\t' +
        str(CHOP780206) + '\t' +
        str(CHOP780207) + '\t' +
        str(EISD860101) + '\t' +
        str(FAUJ880108) + '\t' +
        str(FAUJ880111) + '\t' +
        str(FAUJ880112) + '\t' +
        str(GUYH850101) + '\t' +
        str(JANJ780101) + '\t' +
        str(KRIW790101) + '\t' +
        str(ZIMJ680102) + '\t' +
        str(ONEK900102) + '\t' +
        str(steric_parameter)+'\t'+str(polarizability)+'\t'+str(volume)+'\t'+str(isoelectric_point)+'\t'+str(helix_probability)+'\t'+str(sheet_probability)+'\t'+str(hydrophobicity)+'\t'+str(IS_AMIL)+'\n');
entire.close()
