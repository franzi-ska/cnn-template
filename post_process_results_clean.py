import os
import json

import pandas as pd

import customize_obj

class Inputs:

    local_folder_results = r'D:\BiGART_results'
    local_folder_inputdata = r'D:\BiGART_inputdata'
    local_folder_confics = r'C:\MyGit_Temp\cnn-template\config'

    n_save = 25

    def __init__(self, experiment_name):

        c_file = os.path.join(self.local_folder_confics,
                              experiment_name + '.json')
        with open(c_file) as f:
            d = json.load(f)

        self.datafile = os.path.join(
                    self.local_folder_inputdata,
                    os.path.split(d["dataset_params"]["config"]["filename"])[1]
                    )
        self.val_folds = d["dataset_params"]["config"]["val_folds"]

        self.outputdir = os.path.join(self.local_folder_results, experiment_name)

        n_model = self.pick_model()
        if n_model:
            self.predictionfile = os.path.join(self.local_folder_results, experiment_name,
                                'prediction', 'prediction.{:03}.h5'.format(n_model))
            self.complete = self.check()

        else:
            self.complete = False




    def pick_model(self):
        if not os.path.isfile(os.path.join(self.outputdir, 'logs.csv')):
            print('Logs file does not exist')
            return []
        else:
            log = pd.read_csv(os.path.join(self.outputdir, 'logs.csv'))
            return ((log.shape[0]) // self.n_save) * self.n_save

    def check(self):
        b = True
        if not os.path.isfile(os.path.join(self.local_folder_results, self.predictionfile)):
            print('Prediction file does not exist')
            b= False
        if not os.path.isfile(os.path.join(self.local_folder_inputdata, self.datafile)):
            print('Input data file does not exist')
            b= False
        return b



def analyse_experiment(experiment_name):
    p = Inputs(experiment_name)

    if not p.complete:
        print('Incomplete inputs! -> Skip')
        return

    dice_per_slice = os.path.join( p.outputdir , 'slice.csv')
    dice_per_patient = os.path.join(p.outputdir ,'patient.csv')
    merge_file = os.path.join(p.outputdir,  'merge_images.h5')

    customize_obj.H5MetaDataMapping(
        p.datafile,
        dice_per_slice,
        folds=p.val_folds,
        fold_prefix='fold',
        dataset_names=['patient_ids']
    ).post_process()

    customize_obj.H5CalculateFScore(
        p.predictionfile,
        dice_per_slice
    ).post_process()

    customize_obj.H5Merge2dSlice(
        p.predictionfile,
        dice_per_slice,
        map_column='patient_ids',
        merge_file=merge_file,
        save_file=dice_per_patient
    ).post_process()

    customize_obj.H5CalculateFScore(
        merge_file,
        dice_per_patient,
        map_file=dice_per_patient,
        map_column='patient_ids'
    ).post_process()

def create_combined_fold_patient_csv(dir, n_fold, idx_max,
        prefix = 'bigart_', file='patient.csv'):

    sets_idx = []
    for idx in range(0, idx_max):
        if idx%n_fold == 0:
            sets_idx.append([])
        sets_idx[-1].append(idx)

    for e in sets_idx:

        name = prefix + '_'.join([str(i) for i in e ])

        file_list = [os.path.join(dir, prefix +str(i), file) for i in e]

        if not all([os.path.isfile(f) for f in file_list]):
            print(name, ': missing data')
            continue

        data = pd.concat([pd.read_csv(f, index_col=0) for f in file_list],
                    axis = 0)
        data.to_csv(os.path.join(dir, name+'_'+file))
        # pd.concat(
        #     [
        #     pd.read_csv(os.path.join()
        #     for i in e
        #     ]
        #     )






def main():
    dir = r'D:\BiGART_results'
    # experiment_list = [i for i in os.listdir(dir) if ( i.startswith('bigart_') and not i.endswith('.csv') and not i.startswith('bigart_test')) ]
    # for e in experiment_list:
    #     print(e)
    #     if not os.path.isfile(os.path.join(dir, e, 'patient.csv')):
    #         analyse_experiment(e)
    #     else:
    #         print('\t already done')
    #
    # print('\n\nCombine results\n')
    # create_combined_fold_patient_csv(dir, 5, 125, file='patient.csv')
    # create_combined_fold_patient_csv(dir, 5, 125, file='patient_otherDelineation.csv' )


if __name__ == '__main__':
    main()
