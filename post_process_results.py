import os
import json

import customize_obj


def get_inputs(experiment_id):

    config_file = os.path.join(r'C:\MyGit_Temp\cnn-template\config',
                                experiment_id+'.json')
    with open(config_file) as f:
        json_data = json.load(f)

    datafile_path = os.path.join(
                r'D:\BiGART_inputdata',
                os.path.split(json_data["dataset_params"]["config"]["filename"])[1]
                )

    val_folds = json_data["dataset_params"]["config"]["val_folds"]

    output_folder = os.path.join(r'D:\BiGART_results' , experiment_id )
    if not os.path.isdir(os.path.join(output_folder, 'performance')):
        raise Exception('calculation was not complete for {}'.format(experiment_id))




    p_list = [i for i in os.listdir(os.path.join(output_folder, 'prediction')) if i.endswith('.h5') ]
    p_list.sort() # Make sure the last model is at the end
    prediction_file = os.path.join(output_folder, 'prediction', p_list[-1])

    return output_folder, datafile_path, prediction_file, val_folds

def main(experiment_id):
    output_folder, dataset_file, predicted_h5, val_fold = get_inputs(experiment_id)

    dice_per_slice = os.path.join( output_folder , 'slice.csv')
    dice_per_patient = os.path.join(output_folder ,'patient.csv')
    merge_file = os.path.join(output_folder,  'merge_images.h5')

    customize_obj.H5MetaDataMapping(
        dataset_file,
        dice_per_slice,
        folds=val_fold,
        fold_prefix='fold',
        dataset_names=['patient_ids']
    ).post_process()

    customize_obj.H5CalculateFScore(
        predicted_h5,
        dice_per_slice
    ).post_process()

    customize_obj.H5Merge2dSlice(
        predicted_h5,
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


if __name__ == '__main__':
    print('Start')
    experiment_id = 'bigart_0'
    main(experiment_id)
