import os

import pandas as pd
import matplotlib.pyplot as plt

def box_violin(data, position, color, ax, with_mean=False):
    #plot violin
    parts = ax.violinplot(data, positions=position, vert=False,
                showmeans=False, showmedians=False,showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(color)
        pc.set_alpha(0.4)

    # plot boxplot
    ax.boxplot(data, positions=position, vert=False,
               showmeans=with_mean,
               meanline=True,
               patch_artist=True,
               boxprops=dict(facecolor=color, color='k'),
               medianprops=dict(color='k', ),
               meanprops=dict(color='k',linestyle = ':')
               )

def add_table_text(r_pos, info, data, stats = ['50%', 'IQR']):


    tab  = data.describe()
    print(tab)
    tab['IQR'] = tab['75%'] - tab['25%']
    tab = tab[ stats]

    p_list = ['Dataset', 'Channels','Learning_rate', 'Loss', 'Normalisation', ]
    c_pos_list = [-i for i in range(len(stats) + len(p_list))][::-1]

    for i in range(len(stats)):
        plt.text(r_pos, c_pos[i], tab[stats[i]])
    # for c in c_pos_list


def fig_1():
    marker_folds = ['v', '<', '^', '>', 'D']

    d = pd.read_csv('experiments.csv')
    d.drop_duplicates(subset=d.columns.difference(['ID','validation_fold', 'Status']),
        keep='first', inplace=True)

    src = r'D:\BiGART_results'
    fig, ax =  plt.subplots(1,1, figsize=(5,10))

    p = [i*0.75 for i in range(50)]
    count = 0
    for _, row in d.iterrows():
        file = [i for i in os.listdir(src) if (i.startswith(row['ID']+'_') and i.endswith('.csv'))]

        print(file)
        if len(file) > 1 :
            raise Exception('More than one file')
        elif not file:
            print('Missing ')
            continue
        count += 1

        data = pd.read_csv(os.path.join(src, file[0]))

        color = ('#ff8c00' if row['Dataset'] == 'Oxytarget' else '#78c679')
        box_violin(data['f1_score'].tolist(), [p[count]], color, ax)

        add_table_text(p[count], row, data['f1_score'])

        parts = file[0].split('_')
        for fold, p_sub, m in zip(parts[1:-1], [-0.2, -0.1, 0,  .1, .2], marker_folds):
            fold_data = pd.read_csv(os.path.join(src, parts[0]+'_'+fold, parts[-1]))
            plt.plot(fold_data['f1_score'].median(), p[count]+p_sub,
                    marker = m, color='k', zorder=5000, markersize=5)


    plt.yticks([], '')
    plt.xlabel('DSC$_{P}$')
    plt.show()
fig_1()
