#!/bin/bash

#SBATCH --job-name=EMC
#SBATCH --output=emc-%a.out
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --ntasks-per-socket=2
#SBATCH --cpus-per-task=12
#SBATCH --partition=standard
#SBATCH --qos=user_qos_timeifler
#SBATCH --account=cosmo
#SBATCH --mem-per-cpu=5GB
#SBATCH --time=72:00:00
#SBATCH --array=1-4
#SBATCH --export=none

cd $SLURM_SUBMIT_DIR
source start_cocoa

export OMP_PROC_BIND=close
export OMP_NUM_THREADS=10
mpirun -n 4 --bind-to core --rank-by core --map-by numa:pe=10 cobaya-run ./projects/des_y3/EXAMPLE_EVALUATE${SLURM_ARRAY_TASK_ID}.yaml -f