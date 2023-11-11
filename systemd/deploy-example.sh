#!/bin/bash

#Example Generator
#
#
if [ -z "${1}" ]; then
    echo "Usage: ${0} <user1> [user2]...."
    exit 1
fi  

if [ ! -d deploy ]; then
    mkdir deploy
fi

for user in ${*}; do
    cp -f Path.service deploy/${user}.service
    cp -f Path.path deploy/${user}.path
    sed -i "s/TARGET/${user}/g" deploy/${user}.service deploy/${user}.path
    done
    

    