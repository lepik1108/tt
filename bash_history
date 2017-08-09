#bin/bash/sh

sudo apt-get update

# jenkins
wget -q -O - https://pkg.jenkins.io/debian/jenkins-ci.org.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get install jenkins

# docker
sudo apt-get install docker.io
sudo groupadd docker
sudo usermod -aG docker $(whoami)
sudo usermod -a -G docker jenkins

# mail
sudo apt-get install postfix
sudo apt-get install mailutils

# python
sudo apt-get install bzip2 libreadline6 libreadline6-dev openssl
sudo apt-get install python3 python3-pip python3-openssl



