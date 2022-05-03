#!/usr/bin/env bash



./$1_fp.sh $2 2>&1 | while IFS= read -r line; do
 
 echo $line
if [[ $line == *"Workflow completed"* ]]; 
 then echo "-----------------------------------------------------------------successfully completed workflow"
fi
				
	done
