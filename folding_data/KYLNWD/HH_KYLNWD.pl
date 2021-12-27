#!/usr/bin/perl
use Math::Trig;


##### report node -------->
$time=`date`;
printf "starting time: $time";
$pwd=`pwd`;
printf "pwd: $pwd";




################ directories #############################

$data_dir="/media/stefano/DISCO1/FOLDEN/trRosetta2/example/KYLNWD";  #for seq.txt and init.dat$a3m="!A3M!";
$pdb_db="/media/stefano/DISCO1/FOLDEN/trRosettaX/db_20211124";
$hh_out="/media/stefano/DISCO1/FOLDEN/trRosetta2/example/KYLNWD/protein.out";
$s="KYLNWD";
$fasta="/media/stefano/DISCO1/FOLDEN/trRosetta2/example/KYLNWD/seq.fasta";
$idcut0="1";
$n_temp="10";




########### setup  the environment and Working DIRectory ###
$ENV{'PATH'}="/usr/local/bin:/bin:/usr/bin:/usr/X11R6/bin:/usr/pgi/linux86/bin:";
$ENV{'LD_LIBRARY_PATH'}="/usr/local/lib:/usr/lib:/lib";
$ENV{'HHLIB'}="$bindir";

############### HHP #########################



%ts=(
     'GLY'=>'G',
     'ALA'=>'A',
     'VAL'=>'V',
     'LEU'=>'L',
     'ILE'=>'I',
     'SER'=>'S',
     'THR'=>'T',
     'CYS'=>'C',
     'MET'=>'M',
     'PRO'=>'P',
     'ASP'=>'D',
     'ASN'=>'N',
     'GLU'=>'E',
     'GLN'=>'Q',
     'LYS'=>'K',
     'ARG'=>'R',
     'HIS'=>'H',
     'PHE'=>'F',
     'TYR'=>'Y',
     'TRP'=>'W',

     'ASX'=>'B',
     'GLX'=>'Z',
     'UNK'=>'X',

     'G'=>'GLY',
     'A'=>'ALA',
     'V'=>'VAL',
     'L'=>'LEU',
     'I'=>'ILE',
     'S'=>'SER',
     'T'=>'THR',
     'C'=>'CYS',
     'M'=>'MET',
     'P'=>'PRO',
     'D'=>'ASP',
     'N'=>'ASN',
     'E'=>'GLU',
     'Q'=>'GLN',
     'K'=>'LYS',
     'R'=>'ARG',
     'H'=>'HIS',
     'F'=>'PHE',
     'Y'=>'TYR',
     'W'=>'TRP',

     'a'=>'CYS',
     'b'=>'CYS',
     'c'=>'CYS',
     'd'=>'CYS',
     'e'=>'CYS',
     'f'=>'CYS',
     'g'=>'CYS',
     'h'=>'CYS',
     'i'=>'CYS',
     'j'=>'CYS',
     'k'=>'CYS',
     'l'=>'CYS',
     'm'=>'CYS',
     'n'=>'CYS',
     'o'=>'CYS',
     'p'=>'CYS',
     'q'=>'CYS',
     'r'=>'CYS',
     's'=>'CYS',
     't'=>'CYS',
     'u'=>'CYS',
     'v'=>'CYS',
     'w'=>'CYS',
     'x'=>'CYS',
     'y'=>'CYS',
     'z'=>'CYS',

     'B'=>'ASX',
     'Z'=>'GLX',
     'X'=>'CYS',
    );






################ make fasta sequence file #################
if(!-s "$data_dir/seq.txt"){
	`cp $fasta $data_dir/seq.txt`;
}

@seqtxts=`cat $data_dir/seq.txt`;
$sequence="";
foreach $seqtxt(@seqtxts){
    goto pos6 if($seqtxt=~/\>/);
    $seqtxt=~s/\s//mg;
    $seqtxt=~s/\n//mg;
    $sequence=$sequence.$seqtxt;
  pos6:;
}
$Lch=length $sequence;
if($Lch<=0) {
	print "HOMOLOGY fail... switching back to de novo volding";
	`rm $data_dir/seq.txt`;
	`rm $data_dir/err_HH_*`;
	`rm $data_dir/out_HH_*`;
	`rm $data_dir/process_template_*`;
open(seq,">fail.hmm");
printf seq ">fail.hmm\n";
printf seq "\n";
close(seq);


	print "Exited with fail!"
	exit(-1);
}

open(seq,">protein.seq");
printf seq ">protein\n";
for($i=1;$i<=$Lch;$i++){
    $a=substr($sequence,$i-1,1);
    printf seq "$a";
    $seqQ{$i}=$a;   #only for check
    if($i==int($i/60)*60){
	printf seq "\n";
    }
}
printf seq "\n";
close(seq);



################ calculate Z-score ######################
open(dist,"$hh_out");
$i=0;
while($line=<dist>){
    if($line=~/No Hit                             Prob E-value/){
	while($line=<dist>){
	    goto end_dist if($line=~/^No\s+\d+/);
	    if($line=~/(\d+)\s+(\S+)/){
		$i++;
		$NO{$i}=$1;
		$T_name{$i}=$2;
		$T_prob{$i}=substr($line,35,5);
		$E_value{$i}=substr($line,41,7);
		#$score{$i}=substr($line,58,6);
		$score{$i}=substr($line,57,6);
		$score_a+=$score{$i};
		$score_a2+=$score{$i}**2;
	    }
	}
    }
}
 end_dist:;
close(dist);
$N_hit=$i;
$score_a/=$N_hit;
$score_a2/=$N_hit;
$dev=sqrt($score_a2-$score_a**2);
for($i=1;$i<=$N_hit;$i++){
    $zscore{$i}=-($score_a-$score{$i})/$dev;
    if($i>1){
	if($zscore{$i}>$zscore{$i-1}){
	    $zscore{$i}=$zscore{$i-1}-0.01;
	}
    }
}

###########################################################
##### create template file 'init.dat' #####################
###########################################################
open(temp_info, ">temp_info.dat");    #"%6s %5d %5d %8.3f %6.1f %8s\n"
printf temp_info "%6s %5s %5s %8s %5s %6s %8s\n", "target", "N_good", "N_temp", "z-score", "t_prob", "cov", "E-value";
open(init,">init.dat");
$i_t=0;
for($i=1;$i<=$N_hit;$i++){
    $zscore_value=$zscore{$i};
    $template_name=$T_name{$i};
    $pdb="$pdb_db/$template_name\.pdb";
    goto pos2 if(!-s "$pdb");


	# exclude templates which only contain CA atoms
	@aaa=`cat $pdb`;chomp(@aaa);
	$check_flag = 0;
	foreach $aaa(@aaa)
	{
		next if($aaa!~/^ATOM/);
		if($aaa!~/CA/)
		{
			$check_flag = 1;
		}
	}
	goto pos2 if($check_flag == 0);

    
    ############ check homology ##############
    if($idcut0<0.999){
	$align_rst=`./align protein.seq $pdb 2`;
	if($align_rst=~/Identical length\:\s+(\d+)/){
	    $id=$1/$Lch;
	    goto pos2 if($id>=$idcut0);
	}
    }
    
    ###### read alignment ####################
    open(align,"$hh_out");
    $L_ali=0;
    while($line=<align>){
	#if($line=~/^\>$template_name/){
	if($line=~/^No\s+$NO{$i}/){
	    while($line=<align>){
		goto pos4 if($line=~/No\s+\d+/);
		if($line=~/^Q protein\s+(\d+)\s+(\S+)\s+(\d+)\s+\(/){
		    $nQ=$1-1;
		    $sequenceQ=$2;
		}
		if($line=~/T\s+$template_name\s+(\d+)\s+(\S+)/){
		    $nT=$1-1;
		    $sequenceT=$2;
		    ###
		    $L=length $sequenceT;
		    for($j=1;$j<=$L;$j++){
			$sQ=substr($sequenceQ,$j-1,1);
			$sT=substr($sequenceT,$j-1,1);
			$nQ++ if($sQ ne "-");
			$nT++ if($sT ne "-");
			#if($sQ ne "-" && $sT ne "-"){ # a bug
			if($sQ ne "X" && $sQ ne "-" && $sT ne "-"){
			    $L_ali++;
			    $resQ{$L_ali}=$nQ;
			    $resT{$L_ali}=$nT;
			    $seqQ{$L_ali}=$sQ;
			    $seqT{$L_ali}=$sT;
			}
		    }
		}
	    }
	}
    }
  pos4:;
    close(align);
    
    ############ get coordinates from PDB file ---------->
    open(pdb,"$pdb");
    $n=0;
    $L_ali1=0;
    while($line=<pdb>){
	if(substr($line,12,4)=~/CA/){
	    $n++;
	    substr($line,22,4)=~/(\d+)/;
	    $tmp=$1;
	    ######## check whether the coordinate exist ---------->
	    for($j=1;$j<=$L_ali;$j++){
		if($tmp == $resT{$j}){
		    $L_ali1++;
		    $resQ1{$L_ali1}=$resQ{$j};
		    $seqQ1{$L_ali1}=$seqQ{$j};
		    $resT1{$L_ali1}=$resT{$j};
		    $seqT1{$L_ali1}=$seqT{$j};
		    $xyz{$L_ali1}=substr($line,30,24);
		    ##### check template sequence ----->
		    $tmp1=substr($line,17,3);
		    if($tmp1 ne $ts{$seqT1{$L_ali1}}){
			printf "Template mismatch warning: $template_name: $tmp1 ne $ts{$seqT1{$L_ali1}}!\n";
		    }
		    ##### check query sequence ----->
		    $tmp1=substr($sequence,$resQ1{$L_ali1}-1,1);
		    if($tmp1 ne $seqQ1{$L_ali1}){
			printf "Query mismatch warning: $template_name: $tmp1 ne $seqQ1{$L_ali1}!\n";
		    }
		    goto pos10;
		}
	    }
	  pos10:;
	}
    }
    close(pdb);
    #goto pos2 if($L_ali1/$Lch <0.35);   # Alignement is too short
    goto pos2 if($L_ali1<5);   # Alignement is too short
    
    ############## output init.dat ------------------>
    $i_t++;
    printf init "%5d %8.3f %5d   %6s\n",$L_ali1,$zscore_value,$i_t,$template_name;
    printf temp_info "%6s %5d %5d %8.3f %6.1f %.2f %8s\n", $template_name, $i_t, $NO{$i}, $zscore_value, $T_prob{$i}, $L_ali1/$Lch, $E_value{$i};
    for($j=1;$j<=$L_ali1;$j++){
	printf init "ATOM  %5s  CA  %3s  %4d    %24s%5d %3s\n",
	$j+$i_t*1000,$ts{$seqQ1{$j}},$resQ1{$j},$xyz{$j},$resT1{$j},$ts{$seqT1{$j}};
    }
    printf init "TER\n";
    goto pos3 if($i_t >= $n_temp);
  pos2:;
}
 pos3:;
close(init);
close(temp_info);

open(init1,">init1.dat");
printf init1 "%5d %5d (N_temp, Lch)\n",$i_t,$Lch;
close(init1);
`cat init.dat >>init1.dat`;

my $nlines=`wc -l init1.dat`;
if($nlines=~/^(\d+)/)
{
    $nlines=$1;
}
printf $nlines;
if($nlines<10)
{	
	if(!-e "$data_dir/$s.out"){
		`cp $hh_out $data_dir/`;
	}
}
else
{
    `/bin/mv init1.dat $data_dir/init.HHP`; 	
	if(!-e "$data_dir/$s.out"){
		`cp $hh_out $data_dir/$s.out`;
	}
    `/bin/mv temp_info.dat $data_dir/init.info`;
}


################# endding procedure ######################
my $time=`date`;
printf "ending time: $time";
sleep(1);

exit();

