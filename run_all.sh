#!/usr/bin/bash
#docker pull rapidsai/base:23.08-cuda11.8-py3.10
cd src
make
cd ../graphs
git submodule init
git submodule update
cd PaRMAT/Release
make
cd ../../RMAT
bash test.sh
