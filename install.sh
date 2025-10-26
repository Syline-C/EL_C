#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common net-tools socat lsof gnupg make
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
 | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit.gpg

distribution=$(. /etc/os-release;echo $ID$VERSION_ID)

curl -fsSL https://nvidia.github.io/libnvidia-container/${distribution}/libnvidia-container.list \
 | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit.gpg] https://#' \
 | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list > /dev/null


sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io nvidia-container-toolkit

sudo usermod -aG docker $USER
sudo nvidia-ctk runtime configure --runtime=docker

sudo service docker start
