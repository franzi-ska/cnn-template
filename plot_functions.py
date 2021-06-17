import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def box_violin_plot(data, ax=None, vert=False ):

    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(10,50))

    gridlines = getattr(ax,('axhline' if vert else 'axvline'))
    for p in np.arange(0,1.1, 0.05):
        gridlines(p, alpha=0.1, color='k')


    i=0
    model_ticks, model_tick_labels = [], []
    for key, values in data.items():
        color = ['#ffffcc', '#c2e699','#78c679', '#31a354','#006837'][i%5]
        i +=1
        # plot violin
        parts = ax.violinplot(values, positions=[i], vert=vert,
                      showmeans=False, showmedians=False,showextrema=False)
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_alpha(0.4)
        # plot boxplot
        ax.boxplot(values, positions=[i], vert=vert,
                   showmeans=True, meanline=False, patch_artist=True,
                   boxprops=dict(facecolor=color, color='k'),
                   medianprops=dict(color='k'),
                   meanprops=dict(marker='s', markerfacecolor='k',
                                  markeredgecolor='k', markersize=3)
                   )

        model_tick_labels.append(key)



    dice_tiks = [0, 0.2, 0.4, 0.6, 0.8, 1]
    model_ticks = [i for i in range(1, i+1)]

    plt.xticks((model_ticks if vert else dice_tiks),
                labels = (model_tick_labels if vert else dice_tiks))
    plt.yticks((dice_tiks if vert else model_ticks),
                labels = (dice_tiks if vert else model_tick_labels) )



    plt.xlim(( i+0.5, 0.5,) if vert else (0, 1))
    plt.ylim((0, 1) if vert else ( i+0.5, 0.5))
    plt.show()

def summary_stats(data):

    stats = {}
    for key, values in data.items():
        stats[key] = {}
        stats[key]['dice_patient_mean'] = np.mean(values)
        stats[key]['dice_patient_median'] = np.median(values)
        stats[key]['dice_patient_Q1'] = np.quantile(values, 0.25)
        stats[key]['dice_patient_Q3'] = np.quantile(values, 0.75)



    comb_values = []
    idx = 1
    for key, values in data.items():
        comb_values += values

        # print(len(comb_values))
        if  idx%5 == 0:
            stats[key + 'comb'] = {}
            stats[key + 'comb']['dice_patient_mean'] = np.mean(comb_values)
            stats[key + 'comb']['dice_patient_median'] = np.median(comb_values)
            stats[key + 'comb']['dice_patient_Q1'] = np.quantile(comb_values, 0.25)
            stats[key + 'comb']['dice_patient_Q3'] = np.quantile(comb_values, 0.75)

            comb_values = []


        idx +=1

    pd.DataFrame().from_dict(stats, orient='index').to_csv('experiments_result.csv')


def main():

    # Load data
    src_main = 'D:\BiGART_results'

    data = {}
    result = {}
    for idx in range(40):
        experiment = 'bigart_'+str(idx)
        patient_dice_file = os.path.join(src_main, experiment, 'patient.csv')
        if not os.path.isfile(patient_dice_file):
            print(experiment, ':Missing results')
            data[experiment] = [-1]
            continue
        else:
            data[experiment] = pd.read_csv(patient_dice_file)['f1_score'].to_list()




    # plot the individual folds
    fig, ax = plt.subplots(1,1, figsize=(10,10))
    box_violin_plot(data, vert=False, ax=ax)

    summary_stats(data)



main()
