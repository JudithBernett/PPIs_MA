#!/bin/bash
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --job-name=train_tt_part_human
#SBATCH --output=train_tt_part_human%j.out
#SBATCH --error=train_tt_part_human%j.err
#SBATCH --mem=300G
#SBATCH --time=48:00:00
#SBATCH --partition=compms-gpu-a40
#SBATCH --array=0-8

declare -a combis
index=0
for DATASET in huang pan richoux
do
	for TRAIN in "both" "0"
  	do
		for TEST in "0" "1"
		do
			if [ "$TRAIN" = "0" ] && [ "$TEST" = "0" ]
			then
				continue
			fi
			combis[$index]="$DATASET $TRAIN $TEST"
			index=$((index + 1))
		done 
	done 
done
echo ${combis[*]}

parameters=(${combis[${SLURM_ARRAY_TASK_ID}]})
dataset=${parameters[0]}
train_set=${parameters[1]}
test_set=${parameters[2]}

echo ds: $dataset
echo train: $train_set
echo test: $test_set

{ time dscript train --topsy-turvy --train data/partitions/${dataset}_partition_${train_set}.txt --test data/partitions/${dataset}_partition_${test_set}.txt --embedding /nfs/scratch/jbernett/human_embedding.h5 --save-prefix ./models/${dataset}_${train_set}_${test_set}_tt_partitions -o ./results_topsyturvy/partitions/train_${dataset}_${train_set}_${test_set}.txt; } 2> results_topsyturvy/partitions/train_${dataset}_${train_set}_${test_set}_time.txt
