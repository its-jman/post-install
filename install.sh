#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt install -y python-pip python-dev
pip install setuptools
pip install wheel
pip install git+git://github.com/ansible/ansible.git@devel
# sed -i '1s:.*:#!/usr/bin/python3:' /home/josh/.local/bin/ansible-playbook
export ANSIBLE_NOCOWS=1

ansible-playbook local-configure.yml

chown josh:josh .ansible/ -R
rm -rf ../post-install/
echo "Done with configuration, removed post-install. "
