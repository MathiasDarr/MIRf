#!/bin/bash -ex
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
cd /home/ubuntu

sudo apt update
sudo apt --assume-yes install awscli
aws s3 cp s3://dakobed-guitarset/fileID0/audio.wav .
sudo apt-get --assume-yes install libsndfile1-dev

sudo apt --assume-yes install python3-pip
pip3 install librosa
pip3 install boto3

