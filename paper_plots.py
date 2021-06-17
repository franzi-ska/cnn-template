import os

import pandas as pd
import matplotlib.pyplot as plt

def box_violin(data, position, color, ax):

    if not isinstance(position, list):
        position = [position]
    #plot violin
    parts = ax.violinplot(data, positions=position, vert=False,
                showmeans=False, showmedians=False,showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(color)
        pc.set_alpha(0.4)

    # plot boxplot
    ax.boxplot(data, positions=position, vert=False,
               showmeans=False, meanline=False, patch_artist=True,
               boxprops=dict(facecolor=color, color='k'),
               medianprops=dict(color='k', ),
               # meanprops=dict(color='k',linestyle = ':')
               )


def add_table_line(y, text_info, values,
        include_info,
        include_stats = ['50%', 'IQR']):



    d = values.describe()
    d['IQR'] = d['75%']-d['25%']


    x_list_1 = [-0.1 * (i+1)  for i in range(len(include_stats ))]
    x_list_2 = [-0.15 * (i) + min(x_list_1)-0.15 for i in range(len(include_info))]
    x_list =  x_list_2 + x_list_1
    text = include_info[::-1]+include_stats[::-1]

    if y==0:
        for x, t in zip(x_list, text):
            t = t.replace('Normalisation', 'Norm')\
                 .replace('Learning_rate', 'LR')\
                 .replace('50%', 'M')

            plt.text(x, y-0.5, t, fontweight='bold')

    for x,s  in zip(x_list_1[::-1], include_stats):
        plt.text(x, y,'{:.2f}'.format(d[s]), va='center')

    for x,s  in zip(x_list_2[::-1], include_info):

        t = text_info[s]

        if isinstance(t, float):
            t = '{:.0e}'.format(t)
        else:
            t = t.replace('Z-Score', 'ZS').replace(' ','').replace('ModifiedDiceLoss', 'MDice').replace('BinaryFbetaLoss', 'Dice')
        plt.text(x, y, t, va='center')

def plot_experiment(src, id_0, result, position, row_info, n_fold=5, color='#ff8c00',
    include_info = ['Dataset', 'Channels', 'Normalisation','Learning_rate', 'Loss'],
    include_stats = ['50%', 'IQR']):
    marker_folds = ['v', '<', '^', '>', 'D']


    prefix, idx = id_0.split('_')
    idx = int(idx)

    f_comb = prefix + '_' + '_'.join([str(i) for i in range(idx, idx+n_fold)]) +'_'+result+'.csv'

    main_data = pd.read_csv(os.path.join(src,f_comb))['f1_score']

    box_violin(main_data.to_list(),position,color, plt.gca())


    for i, p in zip(range(n_fold), [-0.2,-0.1, 0, .1, .2]):
        fold_data= pd.read_csv(os.path.join(src,prefix+'_'+str(i+idx),
            result+'.csv'))['f1_score']
        m = fold_data.describe()['50%']
        plt.plot(m, position+p, marker_folds[i]+'k', zorder=5000, markersize=3)

    add_table_line(position, row_info, main_data, include_info, include_stats)


def main():
    src = r'D:\BiGART_results'
    experiment_list = pd.read_csv('experiments.csv')
    experiment_list.drop_duplicates(subset=experiment_list.columns.difference(
                                    ['ID','validation_fold', 'Status']),
                                    keep='first', inplace=True)


    experiment_list = experiment_list.loc[experiment_list['Dataset'].isin(['Oxytarget'])]

    experiment_list.sort_values(['Loss', 'Dataset', 'Channels', 'Normalisation','Learning_rate', ], inplace=True)

    fig, ax = plt.subplots(1,1, figsize=(20,10))
    for idx, (_, e) in enumerate(experiment_list.iterrows()):
        c = '#ff8c00' if e['Dataset']=='Oxytarget' else '#7AD7F0'
        plot_experiment(src, e['ID'], 'patient', idx*0.6, e,  color=c)

    ax.set_ylim(ax.get_ylim()[::-1])
    plt.yticks([], '')
    plt.xticks([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .1])
    plt.xlim([0,1])
    plt.xlabel('DSC$_{P}$')
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.savefig('Fig_paraOpt.png')

    fig, ax = plt.subplots(1,1, figsize=(20,10))
    for idx, (_, e) in enumerate(experiment_list.iterrows()):
        c = '#ff8c00' if e['Dataset']=='Oxytarget' else '#7AD7F0'
        plot_experiment(src, e['ID'], 'patient_otherDelineation', idx*0.6, e,  color=c)
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.yticks([], '')
    plt.xticks([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .1])
    plt.xlim([0,1])
    plt.xlabel('DSC$_{P}$')
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.savefig('Fig_paraOpt_second_delineation.png')


    experiment_list = pd.read_csv('experiments.csv')
    experiment_list.drop_duplicates(subset=experiment_list.columns.difference(
                                    ['ID','validation_fold', 'Status']),
                                    keep='first', inplace=True)
    experiment_list = experiment_list.loc[experiment_list['Dataset'].isin(['LARC'])]
    experiment_list.sort_values(['Loss', 'Dataset', 'Channels', 'Normalisation','Learning_rate', ], inplace=True)
    fig, ax = plt.subplots(1,1, figsize=(20,10))
    for idx, (_, e) in enumerate(experiment_list.iterrows()):
        c = '#ff8c00' if e['Dataset']=='Oxytarget' else '#7AD7F0'
        plot_experiment(src, e['ID'], 'patient', idx*0.6, e,  color=c)
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.yticks([], '')
    plt.xticks([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .1])
    plt.xlim([0,1])
    plt.xlabel('DSC$_{P}$')
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.savefig('Fig_LARC.png')

    #%% Test results

    experiment_list = pd.read_csv('experiments.csv')
    experiment_list.drop_duplicates(subset=experiment_list.columns.difference(
                                    ['ID','validation_fold', 'Status']),
                                    keep='first', inplace=True)


    experiment_list = experiment_list.loc[experiment_list['Dataset'].isin(['Oxytarget'])]\
                        .loc[experiment_list['fold'].isin([1])]


    experiment_list.sort_values(['Loss', 'Dataset', 'Channels', 'Normalisation','Learning_rate', ], inplace=True)

    fig, ax = plt.subplots(1,1, figsize=(20,10))
    for idx, (_, e) in enumerate(experiment_list.iterrows()):
        c = '#ff8c00' if e['Dataset']=='Oxytarget' else '#7AD7F0'
        plot_experiment(src, e['ID'], 'prediction_test_voted', idx*0.6, e,  color=c, n_fold = 1)

    ax.set_ylim(ax.get_ylim()[::-1])
    plt.yticks([], '')
    plt.xticks([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .1])
    plt.xlim([0,1])
    plt.xlabel('DSC$_{P}$')
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.savefig('Fig_paraOpt.png')

if __name__ == '__main__':
    main()
