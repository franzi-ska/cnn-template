#!/bin/bash
#SBATCH --nodes=1                # Use 1 node
#$SBATCH --ntasks-per-node=1
#SBATCH --job-name=bigart_test   # sensible name for the job
#SBATCH --mem=16G                 # Default memory per CPU is 3GB.
#SBATCH --partition=gpu # Use the verysmallmem-partition for jobs requiring < 10 GB RAM.
#SBATCH --gres=gpu:1
#SBATCH --mail-user=franziska.h.knuth@ntnu.no # Email me when job is done.
#SBATCH --mail-type=ALL
#SBATCH --output=outputs/bigart_test_%a__%A.out
#SBATCH --error=outputs/bigart_test_%a__%A.out

## Below you can put your scripts
# If you want to load module
module load singularity

## Code
# If data files aren't copied, do so
#!/bin/bash


if [ ! -d "$TMPDIR/$USER/hn_delin" ]
    then
    echo "Didn't find dataset folder. Copying files..."
    mkdir --parents $TMPDIR/$USER/hn_delin
    fi

for f in $(ls $HOME/datasets/*)
    do
    FILENAME=`echo $f | awk -F/ '{print $NF}'`
    echo $FILENAME
    if [ ! -f "$TMPDIR/$USER/hn_delin/$FILENAME" ]
        then
        echo "copying $f"
        cp -r $HOME/datasets/$FILENAME $TMPDIR/$USER/hn_delin/
        fi
    done


echo "Finished seting up files."

# Hack to ensure that the GPUs work
nvidia-modprobe -u -c=0

# Run test on external data
singularity exec --nv deoxys-beta.sif python -u test_experiment_external.py config/bigart_test_$SLURM_ARRAY_TASK_ID.json $HOME/performance/bigart_$SLURM_ARRAY_TASK_ID  $HOME/bigart_models/bigart_$SLURM_ARRAY_TASK_ID.h5 
