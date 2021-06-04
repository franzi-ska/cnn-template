import os
import shutil
import sys

import csv




def read_cvs(csv_file_path):

    csv_file_path = r'C:\Users\franzihk\Downloads\bigart_0\logs.csv'
    with open(csv_file_path) as f:
        spamreader = csv.reader(f)
        for row in spamreader:
            print(row)


experiment = sys.argv[1]

src_main = r'/net/fs-1/home01/franzikn/performance'
dst_main = r'/net/fs-1/home01/franzikn/performance_cleaned'
path_log_file = os.path.join(src_main, experiment, 'logs.csv')

log = pd.read_csv(path_log_file)
n_best = log['val_dice'].idxmax() +1 #+1 to go from epoch to model index
save_suffix = '.{:03d}.h5'.format(n_best)


files_of_interest =  [
            ('logs.csv' , 'logs.csv'),
            (os.path.join('model', 'model'+save_suffix), 'model.h5'),
            (os.path.join('prediction', 'prediction'+save_suffix), 'prediction.h5'),
            (os.path.join('performance', 'all.png'), 'performance_all.png')
        ]
folder_of_interest= [
        (os.path.join('images', 'prediction'+save_suffix), 'images')
        ]

for (src_folder, dst_folder) in folder_of_interest:
    shutil.copytree(
        os.path.join(src_main, experiment, src_folder),
        os.path.join(dst_main, experiment, dst_folder)
    )

for (src_file, dst_file) in files_of_interest:
    shutil.copy(
        os.path.join(src_main, experiment, src_file),
        os.path.join(dst_main, experiment, dst_file)
    )

# delete the src folder os.path.join(src_main, experiment)
os.rmdir(os.path.join(src_main, experiment))
