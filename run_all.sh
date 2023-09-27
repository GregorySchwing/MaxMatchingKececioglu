#!/usr/bin/bash
cd src
make
cd ../graphs
git submodule init
git submodule update
cd PaRMAT/Release
make
cd ../../RMAT
bash test.sh
