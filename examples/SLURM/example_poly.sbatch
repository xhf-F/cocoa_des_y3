#!/bin/bash

#SBATCH --job-name=EP_DY3
#SBATCH --output=epoly-%a.out
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=22
#SBATCH --ntasks-per-socket=11
#SBATCH --cpus-per-task=4
#SBATCH --partition=standard
#SBATCH --qos=user_qos_timeifler
#SBATCH --account=cosmo
#SBATCH --mem-per-cpu=5GB
#SBATCH --time=72:00:00
#SBATCH --export=none
#SBATCH --exclusive

echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo Slurm job NAME is $SLURM_JOB_NAME
echo Slurm job ID is $SLURM_JOBID

cd $SLURM_SUBMIT_DIR
source start_cocoa

export OMP_PROC_BIND=close
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
mpirun --mca pml ob1 --mca btl ^openib -n ${SLURM_NTASKS} --bind-to core --rank-by core --map-by numa:pe=${OMP_NUM_THREADS} cobaya-run ./projects/des_y3/EXAMPLE_POLY${SLURM_ARRAY_TASK_ID}.yaml -r