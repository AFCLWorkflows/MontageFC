#!/usr/bin/env bash



for value in {1..10}
do
	 timeout 7m java -jar enactment-engine-all.jar montage_fp_backup2.yaml input_montage_$1p.json & 

done
for value in {1..10}
do
	timeout 7m  java -jar enactment-engine-all.jar montage_fp_backup2.yaml input_montage_$1p.json & 

done
for value in {1..10}
do
	timeout 7m java -jar enactment-engine-all.jar montage_fp_backup2.yaml input_montage_$1p.json & 

done


echo All done

