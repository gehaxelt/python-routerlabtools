#!/bin/bash



display_usage() { 
	echo "This script must be run with super-user privileges." 
	echo -e "\nUsage:\n reset.sh <cloud-prefix> \n" 
}

# if less than two arguments supplied, display usage 
	if [  $# -le 0 ] 
	then 
		display_usage
		exit 1
	fi 
 
# check whether user had supplied -h or --help . If yes display usage 
	if [[ ( $# == "--help") ||  $# == "-h" ]] 
	then 
		display_usage
		exit 0
	fi

for d in $1-{rc1,rj2,rj1,sc1,sj1}; do python ./loadconfig.py "$d" "clean/$d"; done
