After forking this repository, replace `orion_username` in the file `2d_unet_CT_W_PET.json` with your actual orion username.


# Setup in Orion cluster
The `$HOME` directory of your login machine (`[username@login ~]`) should have the following structure
```
$HOME
   ├── cnn_template (the forked repository)
   │   ├── config
   │   |   ├── 2d_unet.json
   │   |   └── (other configurations)
   |   ├── outputs
   │   |   └── README.md
   │   ├── customize_obj.py
   │   ├── experiment.py
   │   ├── slurm.sh
   │   ├── setup.sh
   │   └── (other files)
   ├── datasets (Put your datasets in here)
   │   └── headneck
   │       ├── full_dataset_singleclass.h5
   │       └── (other datasets)
   ├── hnperf (log files will be saved in here)
   │
```
Start by running `setup.sh` to download the singularity container
```bash
cd cnn-template
./setup.sh
```
Alternative you can directly download the image file
```bash
cd cnn-template
singularity pull --name deoxys.sif shub://huynhngoc/head-neck-analysis
```

# Run experiments on Orion

## Submit jobs
Submit slurm jobs like this:

```bash
sbatch slurm.sh config/2d_unet.json 2d_unet 200
```

Which will load the setup from the `config/2d_unet.json` file, train for 200 epochs
and store the results in the folder `$HOME/hnperf/2d_unet/`.

To customize model and prediction checkpoints, add the `model_checkpoint_period` and `prediction_checkpoint_period` as arguments

```bash
sbatch slurm.sh config/2d_unet_CT_W_PET.json 2d_unet_CT_W_PET 100 --model_checkpoint_period 5 --prediction_checkpoint_period 5

```
Which will save the trained model every 5 epochs and predict the validation set every 5 epoch

## Continue experiments and run test

To continue an experiment
```bash
sbatch slurm_cont.sh ../hnperf/2d_unet_CT_W_PET/model/model.030.h5 2d_unet_CT_W_PET 100 --model_checkpoint_period 5 --prediction_checkpoint_period 5
```
Which will load the saved model and continue training 100 more epochs


In the case the job ended unexpectedly before plotting the performance:
```bash
sbatch slurm_vis.sh 2d_unet_CT_W_PET
```

To run test
```bash
sbatch slurm_test.sh ../hnperf/2d_unet_CT_W_PET/model/model.030.h5 2d_unet_CT_W_PET
```

To run external validation
```bash
sbatch slurm_external.sh ../hnperf/2d_unet_CT_W_PET/model/model.030.h5 2d_unet_CT_W_PET_maastro maastro.json
```


# Misc

Manually build the singularity image file
```
singularity build --fakeroot Singularity deoxys.sif
```

Login to a gpu session to use the gpu
```bash
qlogin --partition=gpu --gres=gpu:1
singularity exec --nv deoxys.sif ipython
```
