#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt install virtualenv
virtualenv /tmp/installation-venv/
source /tmp/installation-venv/bin/activate
pip install ansible

ansible-playbook local-configure.yml

deactivate
rm -rf /tmp/installation-venv/
rm -rf ../post-install/
echo "\nDone with configuration, removed post-install. "
cd ../
