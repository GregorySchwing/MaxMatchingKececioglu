#!/bin/bash

#SBATCH --job-name down 

#SBATCH -N 1

#SBATCH -n 1 

#SBATCH --mem=10G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=go2432@wayne.edu
#SBATCH --nodelist=reslab32ai8111

#SBATCH -o output_%j.out

#SBATCH -e errors_%j.err

#SBATCH -t 7-0:0:0
#eval "$(conda shell.bash hook)"
echo $HOSTNAME
cd ../graphs/dimacs
bash download_all.txt
