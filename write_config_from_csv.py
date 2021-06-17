import json
import shutil
import os

import pandas as pd


def copy_model(experiment):
    n_save = 25
    src = 'D:\BiGART_results'
    log = pd.read_csv(os.path.join(src, experiment, 'logs.csv'))
    n_model = ((log.shape[0]) // n_save) * n_save

    print(experiment, n_model)

    shutil.copyfile(
        os.path.join(src, experiment, 'model', 'model.{:03}.h5'.format(n_model)),
        os.path.join('D:\BigART_models', experiment+'.h5')
    )


def write_file(h5_file, n_channel, test_fold, learning_rate, config_filename, loss):
    template_config = 'bigart_template.json'
    with open(template_config) as f:
        json_data_template = json.load(f)

    fold_list = [1, 2, 3, 4, 5]
    json_data_template["dataset_params"]["config"]["filename"] = h5_file
    json_data_template["dataset_params"]["config"]["test_folds"] = [
    str(test_fold) + "/352"]
    json_data_template["dataset_params"]["config"]["val_folds"] = [
    str(test_fold) + "/352"]
    json_data_template["dataset_params"]["config"]["train_folds"] = [
    str(i) + "/352" for i in fold_list if not i == test_fold]

    json_data_template["input_params"]["shape"] = [352, 352, n_channel]
    json_data_template["model_params"]['optimizer']['config']['learning_rate'] = learning_rate
    json_data_template["model_params"]["loss"]["class_name"] = loss
    # write file to disk
    with open(config_filename, 'w') as json_file:
        json.dump(json_data_template, json_file)


def read_csv_and_write_config_files():
    data = pd.read_csv('experiments.csv')


    for (row_id, row) in data.iterrows():
        print(row_id)
        h5_file = '/net/fs-1/home01/franzikn/datasets/'
        config_filename = os.path.join( 'config', row['ID']+'.json')
        test_fold = row['validation_fold']
        learning_rate = row['Learning_rate']
        loss = row['Loss']

        if isinstance(row['datafile'], str):
            h5_file += row['datafile']
            n_channel = 1

        else:
            if row['Dataset'] == 'Oxytarget':
                h5_file += 'OxyTarget_'
            elif row['Dataset'] == 'LARC':
                h5_file += 'LARC_'
            if row['Channels'] == 'T2w':
                n_channel = 1
                h5_file += 'T2_'
            elif row['Channels'] == 'T2w + DW':
                n_channel = 2
                h5_file += 'T2DW_'
            else:
                raise Exception('Check for typos in Channels')

            if row['Normalisation'] == 'Z-Score':
                h5_file += 'ZScore.h5'
            elif row['Normalisation'] == 'Z-Score + HM':
                h5_file += 'MHZScore.h5'
            elif row['Normalisation'] == 'Z-Score + HM_onLARC':
                h5_file += 'MHZScore_onLARC.h5'
            elif row['Normalisation'] == 'Z-Score + HM_onOxy':
                h5_file += 'MHZScore_onOxy.h5'

            else:
                raise Exception('Check for typos in Normalisation')

        write_file(h5_file, n_channel, test_fold, learning_rate, config_filename, loss)




def write_test_config():
    for id in [0,1,2,3,4,
               10,11,12,13,14,
               55,56,57,58,59,
               65,66,67,68,69]:

        with open('bigart_test_template.json') as f:
            temp = json.load(f)
        with open(os.path.join('config','bigart_{}.json'.format(id))) as f:
            config = json.load(f)
        file = config["dataset_params"]["config"]["filename"]
        file_parts = file.split('.')
        temp['config']['filename'] = file_parts[0]+'_wTest.'+file_parts[1]

        with open(os.path.join('config','bigart_test_{}.json'.format(id)), 'w') as f:
            json.dump(temp, f)

        # copy_model('bigart_'+str(id))

# read_csv_and_write_config_files()
# write_test_config()
# copy_model('bigart_0')

for i in range(5):
    copy_model('bigart_{}'.format(115+i))
