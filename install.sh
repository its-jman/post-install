#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt update
apt install -y software-properties-common apt-transport-https

# Only add repo if it is not already added (Does this work?)
if ! grep ^ /etc/apt/sources.list /etc/apt/sources.list.d/* | grep -q ansible; then
  apt-add-repository -y ppa:ansible/ansible
fi

apt update
apt upgrade -y
apt install -y python-pip python-dev ansible
#pip install -r requirements.txt
pip install setuptools
pip install wheel
pip install requests
pip install lxml
export ANSIBLE_NOCOWS=1
export ANSIBLE_RETRY_FILES_ENABLED=0

ansible-playbook local-configure.yml

# rm -rf ../post-install/
echo "Done with configuration" # , removed post-install. "
