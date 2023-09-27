#!/usr/bin/bash
docker run --gpus all --rm -it -p 8888:8888 -u root -p 8787:8787 -p 8786:8786 rapidsai/base:23.08-cuda11.8-py3.10 bash
apt-get update && apt-get upgrade && apt-get install git

