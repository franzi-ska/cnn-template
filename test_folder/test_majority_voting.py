import os

import h5py
import numpy as np
import pandas as pd

def calc_dice(X, Y):
    if X.any() or Y.any():
        d = 2* np.count_nonzero(np.logical_and(X, Y)) / (np.count_nonzero(X)+np.count_nonzero(Y))
    else:
        d=0
    return d


def voted_prediction(idx0):

    n_fold = 5
    files = [h5py.File(
                os.path.join('D:\BiGART_results',
                             '2d__LARC_testset_bigart_{}'.format(idx0+i),
                             'test',
                             'prediction_test.h5'),
                'r') for i in range(n_fold)]


    patient_list = files[0]['predicted'].keys()

    dice_GT = []
    res_h5 = h5py.File(r'D:\BiGART_results\'voted_testset_LARC_{}.h5'.format(idx0), 'w')
    res_h5.create_group('predicted')
    res_h5.create_group('x')
    res_h5.create_group('y')

    for p in patient_list:
        voted_prediction = (files[0]['predicted'][p][:,:,:,:] +
                            files[1]['predicted'][p][:,:,:,:] +
                            files[2]['predicted'][p][:,:,:,:] +
                            files[3]['predicted'][p][:,:,:,:] +
                            files[4]['predicted'][p][:,:,:,:]) * 0.2
        gt = files[0]['y'][p][:,:,:,:]

        res_h5['predicted'].create_dataset(p, data=voted_prediction)
        res_h5['y'].create_dataset(p, data=gt)
        res_h5['x'].create_dataset(p, data=files[0]['x'][p][:,:,:,:])

        dice_GT.append([p,
                        calc_dice(voted_prediction.flatten() >0.5,
                                  gt.flatten() )
                       ])


    pd.DataFrame(dice_GT,
                columns=['patient_ids', 'f1_score']).to_csv(
        os.path.join(r'D:BiGART_results', 'voted_testset_LARC_{}.csv'.format(idx0)))



    [f.close() for f in files]
    res_h5.close()

#
def other_delineation(idx0):

    pred = h5py.File(r'D:\BiGART_results\voted_{}.h5'.format(idx0), 'r')
    gt = h5py.File(r'D:\BiGART_inputdata\OxyTarget_Delineation2.h5', 'r')




    patient_list = [i for i in pred['predicted'].keys()]

    gt_slice_list_patients = set([int(i) for i in gt['fold_6/352']['patient_ids']])
    #
    # print(type(patient_list[0]))
    # print(type(gt_slice_list_patients[0]))

    for patient in patient_list:



        if int(float(patient)) in set(gt_slice_list_patients):
            print(patient, 'yes')
            prediction_patient = pred['predicted'][patient][:,:,:,:].flatten()

        else:
            print(patient, 'no')



    pred.close()
    gt.close()


if __name__ == '__main__':
    # voted_prediction(10)
    # voted_prediction(55, 'ZScore')
    # voted_prediction(55, 'MHZScore_onLARC')
    voted_prediction(115)
    # other_delineation(10)
