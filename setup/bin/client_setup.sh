#!/bin/bash

# From https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#os-requirements

# Uninstalling old docker versions if any
sudo apt-get remove docker docker-engine docker.io
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install -y docker-ce

sudo service docker start

# so user can run docker commands withouts sudo
usermod -a -G docker thota

# testing
docker ps
