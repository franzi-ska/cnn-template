#!/bin/bash
#SBATCH --nodes=1                # Use 1 node
#$SBATCH --ntasks-per-node=1
#SBATCH --job-name=bigart   # sensible name for the job
#SBATCH --mem=8G                 # Default memory per CPU is 3GB.
#SBATCH --partition=gpu # Use the verysmallmem-partition for jobs requiring < 10 GB RAM.
#SBATCH --gres=gpu:1
#SBATCH --mail-user=franziska.h.knuth@ntnu.no # Email me when job is done.
#SBATCH --mail-type=ALL
#SBATCH --output=outputs/bigart_%a__%A.out
#SBATCH --error=outputs/bigart_%a__%A.out

# If you would like to use more please adjust this.


## Below you can put your scripts
# If you want to load module
module load singularity

## Code
# If data files aren't copied, do so
#!/bin/bash
# if [ $# -lt 1 ];
#     then
#     printf "Not enough arguments - %d\n" $#
#     exit 0
#     fi

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


# Run experiment
singularity exec --nv deoxys.sif python experiment.py config/bigart_$SLURM_ARRAY_TASK_ID.json $HOME/performance/bigart_$SLURM_ARRAY_TASK_ID --epochs 200
