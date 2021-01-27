#!/bin/bash

echo "Starting experiments at: [ "$(date) "]"

nonomino_id=( 00 13 23 30 59 )
array=( 10 15 20 25 30 )

for id in "${nonomino_id[@]}"
do
	echo 'Starting experiments with nonomino n8_'"$id" at $(date +'%Y-%m-%d %H:%M:%S')
	for i in "${array[@]}"
	do
		echo '    Starting experiment n8_'"$id"_"$i" at $(date +'%Y-%m-%d %H:%M:%S')
		
		python GA_experiment_nonomino.py inputs/n8_"$id"/n8_"$id"_"$i"empty.txt > outputs/n8_"$id"/n8_"$id"_"$i"empty_experiment_$(date +'%Y-%m-%d_%H-%M-%S')_result.log
		
		echo '    Finished experiment n8_'"$id"_"$i" at $(date +'%Y-%m-%d %H:%M:%S')
		echo
	done

	echo 'Finished experiments with nonomino n8_'"$id" at $(date +'%Y-%m-%d %H:%M:%S')
	echo
done