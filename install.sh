#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt install python3-pip python3-dev
pip3 install setuptools
pip3 install wheel
pip3 install git+git://github.com/ansible/ansible.git@devel
sed -i '1s:.*:#!/usr/lib/python3:' /home/josh/.local/bin/ansible-playbook
export ANSIBLE_NOCOWS=1

ansible-playbook local-configure.yml

deactivate
rm -rf ../post-install/
echo "Done with configuration, removed post-install. "
