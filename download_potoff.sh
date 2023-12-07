#!/bin/bash

#SBATCH --job-name down 

#SBATCH -N 1

#SBATCH -n 1 

#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=go2432@wayne.edu

#SBATCH -o output_%j.out

#SBATCH -e errors_%j.err

#SBATCH -t 7-0:0:0
#eval "$(conda shell.bash hook)"
echo $HOSTNAME
bash graphs/dimacs/download_all.txt
