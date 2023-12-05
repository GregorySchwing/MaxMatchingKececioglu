git submodule update --init --recursive
git submodule update --recursive --remote
cd src
make
./matching MT=9 IF=../graphs/test_cases/blossreq.txt

