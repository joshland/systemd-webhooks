#!/bin/bash

function fail(){
    echo "FAILED: $*"
    exit
}

BASE=/srv/webhooks/waitressd
VENV=${BASE}/venv
mkdir -p ${BASE}

pushd ${BASE}

#
# Ansible bootstrapper
#
if [ -e ${VENV} ]; then
    echo "Purge old env"
    rm -fR ${VENV}/
fi

if [ -e activate ]; then
    echo "Remove old shortcut"
    rm activate
fi

echo 'Build Virtual Env'
python3 -m venv ${VENV} > local.log || fail "Virtual Environment build failed"
source ${VENV}/bin/activate
pip install --upgrade pip wheel >> local.log || fail "Failed to Update PIP and Wheel."
pip install --upgrade -r requirements.txt >> local.log || fail "Failed to Install requirements."

ln -s ${VENV}/bin/activate activate > /dev/null

echo ''
echo "Probably complete"
echo 'to enter the env: `source ${VENV}/bin/activate`'
echo '-or-'
echo 'use the shortcut: `source activate`'
