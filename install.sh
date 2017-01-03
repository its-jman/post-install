#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt install -y python-pip python-dev
pip install setuptools
pip install wheel
pip install git+git://github.com/ansible/ansible.git@devel
export ANSIBLE_NOCOWS=1

ansible-playbook local-configure.yml

# TODO: This needs to be dynamic
chown josh:josh .ansible/ -R
rm -rf ../post-install/
echo "Done with configuration, removed post-install. "
