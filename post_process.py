import customize_obj


if __name__ == '__main__':
    output_folder = '../outputs/' # change this to the folder you want to store the result
    dataset_file = '../../full_dataset_singleclass.h5' # path to the dataset

    predicted_h5 = '../../hn_perf/2d_unet/prediction/prediction.020.h5' # the prediction file you want to calculate the dice

    dice_per_slice = output_folder + 'slice.csv'
    dice_per_patient = output_folder + 'patient.csv'
    merge_file = output_folder + 'merge_images.h5'

    customize_obj.H5MetaDataMapping(
        dataset_file,
        dice_per_slice,
        folds=['val'], # change this to ['test'] if you want to calculate the dice of the test prediction
        fold_prefix='',
        dataset_names=['patient_idx', 'slice_idx']
    ).post_process()

    customize_obj.H5CalculateFScore(
        predicted_h5,
        dice_per_slice
    ).post_process()

    customize_obj.H5Merge2dSlice(
        predicted_h5,
        dice_per_slice,
        map_column='patient_idx',
        merge_file=merge_file,
        save_file=dice_per_patient
    ).post_process()

    customize_obj.H5CalculateFScore(
        merge_file,
        dice_per_patient,
        map_file=dice_per_patient,
        map_column='patient_idx'
    ).post_process()
