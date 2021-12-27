clear
deltab all
ForceField AMBER14,SetPar=No
Longrange None
Cutoff 10.50000
Interactions Bond,Angle,Dihedral,Planarity,Coulomb,VdW  
pH = 7.4


macrotarget = 'C:\Users\Utente\Desktop\tabulate_luigi' ###inserisci il tuo path
MakeTab 1,Dimensions=1

for id in file (Macrotarget)\lista_pdb.txt ###crea un lista con i nomi dei tuoi pdb
  delobj all
  loadpdb (macrotarget)\(id).pdb
  clean
  carica = Charge
  en_bond = EnergyObj 1,Bond
  en_angle = EnergyObj 1,Angle
  en_dihedral = EnergyObj 1,Dihedral
  en_Planarity = EnergyObj 1,Planarity
  en_Coulumb = EnergyObj 1,Coulomb
  en_VdW = EnergyObj 1,VdW
  massa_prot = MassObj 1
  volume_prot_VdW = VolumeObj 1,Type=VdW 
  volume_prot_molecular = VolumeObj 1,Type=Molecular
  volume_prot_access = VolumeObj 1,Type=Accessible
  raggio_prot = RadiusObj 1,Center=geometric,Type=VdW

  tabulate '(id)'
  tabulate (0.00+carica)
  tabulate (0.00+en_bond)
  tabulate (0.00+en_angle) 
  tabulate (0.00+en_dihedral) 
  tabulate (0.00+en_Planarity) 
  tabulate (0.00+en_Coulumb) 
  tabulate (0.00+en_VdW) 
  tabulate (0.00+massa_prot)
  tabulate (0.00+volume_prot_VdW) 
  tabulate (0.00+volume_prot_molecular)
  tabulate (0.00+volume_prot_access)
  tabulate (0.00+raggio_prot)
  residui = countres aminoacid
  for i = 1 to residui
    carica_res = chargeres (i)
    en_bond_res = Energyres (i),Bond
    en_angle_res = Energyres (i),Angle
    en_dihedral_res = Energyres (i),Dihedral
    en_Planarity_res = Energyres (i),Planarity
    en_Coulumb_res = Energyres (i),Coulomb
    en_VdW_res = Energyres (i),VdW
    massa_res = Massres (i)
    volume_res_VdW = Volumeres (i),Type=VdW 
    volume_res_molecular = Volumeres (i),Type=Molecular
    volume_res_access = Volumeres (i),Type=Accessible
    raggio_res = Radiusres (i),Center=geometric,Type=VdW
    tabulate (0.00+carica_res) 
    tabulate (0.00+en_bond_res) 
    tabulate (0.00+en_angle_res) 
    tabulate (0.00+en_dihedral_res) 
    tabulate (0.00+en_Planarity_res) 
    tabulate (0.00+en_Coulumb_res) 
    tabulate (0.00+en_VdW_res) 
    tabulate (0.00+massa_res)
    tabulate (0.00+volume_res_VdW) 
    tabulate (0.00+volume_res_molecular)
    tabulate (0.00+volume_res_access)
    tabulate (0.00+raggio_res)
  
SaveTab 1, (Macrotarget)\dati_luigi.txt,Format=Text\t,Columns=(((residui)*12)+13),NumFormat=6.2f, id carica en_bond en_angle en_dihedral en_Planarity en_Coulumb en_VdW massa_prot volume_prot_VdW volume_prot_molecular volume_prot_access raggio_prot carica_res en_bond_res en_angle_res en_dihedral_res en_Planarity_res en_Coulumb_res en_VdW_res massa_res volume_res_VdW volume_res_molecular volume_res_access raggio_res

showmessage 'i tuoi dati sono qui (Macrotarget)\dati_luigi.txt'