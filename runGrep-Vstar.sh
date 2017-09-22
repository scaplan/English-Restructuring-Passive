#!/bin/bash  

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/English-Restructuring-Passive/'
directorySource='/mnt/pollux-new/cis/nlp/data/corpora/COCA/Word_lemma_PoS'
#resultSource='/mnt/nlpgridio2/nlp/users/spcaplan/phrasalVerbs-output'

cd $scriptSource

## Sub-Corpora
	# acad_
	# fic_
	# mag_
	# news_
	# spok_
subCorpora=("acad_" "fic_" "mag_" "news_" "spok_")
#subCorpora=("spok_")

background_PID_list=()

for currSubCorpus in "${subCorpora[@]}"; do
	echo 'Starting (background): '$currSubCorpus
	#python identifyPhrasalVerbs.py $directorySource $currSubCorpus $resultSource &
	
	python newPassiveGrep-Vstar.py $directorySource $currSubCorpus
	echo '\n'
#	LAST_PID=$!
#	background_PID_list+=($LAST_PID)
done

#for backgroun_PID in "${background_PID_list[@]}"; do
#	wait $backgroun_PID
#done

echo 'Completed'