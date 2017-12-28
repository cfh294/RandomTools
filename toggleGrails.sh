#!/bin/bash

# require sudo 
if [[ $UID != 0 ]]; then
    echo "Must be run with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

# I have grails installed in local, others may have it in /usr/share
cd /usr/local
currentGrails=$(readlink grails)

if [ -z $currentGrails ]; then
	echo "No 'grails' link configured."
	exit 1
fi

if [[ ! -d "grails-$1" ]]; then
	echo "The version you chose ($1) is not installed on your system."
	exit 1
fi

newGrails="grails-$1"
if [ $currentGrails == "$newGrails/" ]; then
	echo "Grails is already set to that version."
else
	echo "Grails now set to version $1"
	rm grails
    ln -s $newGrails/ grails
fi