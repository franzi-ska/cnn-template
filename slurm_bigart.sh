#!/bin/bash
#SBATCH --ntasks=1               # 1 core(CPU)
#SBATCH --nodes=1                # Use 1 node
#SBATCH --job-name=bigart   # sensible name for the job
#SBATCH --mem=8G                 # Default memory per CPU is 3GB.
#SBATCH --partition=gpu # Use the verysmallmem-partition for jobs requiring < 10 GB RAM.
#SBATCH --gres=gpu:1
#SBATCH --mail-user=franziska.h.knuth@ntnu.no # Email me when job is done.
#SBATCH --mail-type=ALL
#SBATCH --output=outputs/training_%A.out
#SBATCH --error=outputs/training_%A.out




# If you would like to use more please adjust this.


echo $1


## Below you can put your scripts
# If you want to load module
module load singularity
# module load Python/3.8.2-GCCcore-9.3.0
## Code
# If data files aren't copied, do so
#!/bin/bash
if [ $# -lt 1 ];
    then
    printf "Not enough arguments - %d\n" $#
    exit 0
    fi

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
singularity exec --nv deoxys.sif python experiment.py config/$1.json $HOME/performance/$1 --epochs 200  ${@:2}

# copy the relevant files to _cleaned folder
# python copy_result.py $1
