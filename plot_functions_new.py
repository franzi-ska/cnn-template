#%%
import os


import pandas as pd
import matplotlib.pyplot as plt

def box_violin(data, position, color, ax):
    #plot violin
    parts = ax.violinplot(data, positions=position, vert=False,
                showmeans=False, showmedians=False,showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(color)
        pc.set_alpha(0.4)

    # plot boxplot
    ax.boxplot(data, positions=position, vert=False,
               showmeans=True, meanline=True, patch_artist=True,
               boxprops=dict(facecolor=color, color='k'),
               medianprops=dict(color='k', ),
               # meanprops=dict(color='k',linestyle = ':')
               )

def get_data(src_main, include_idx=range(45), prefix='bigart_', file='patient.csv',
             column='f1_score'):
    dataset = {}
    for i in include_idx:
        name = prefix + str(i)
        src = os.path.join(src_main, name, file)
        dataset[name] = pd.read_csv(src, index_col=0)

    return dataset

def combine_folds(data, prefix='bigart_',
        n_experiment=11, idx_start=0, size_fold = 5):

    a = idx_start
    b = idx_start+size_fold

    data_c = {}

    for i in range(n_experiment):
        combine_idx = range(a, b)
        name = prefix + '_'.join([str(i) for i in combine_idx])
        data_c[name] = pd.concat([data[prefix+str(i)] for i in combine_idx])
        a += 5
        b += 5
    return data_c


def add_table(ax, tab):

    tab['IQR'] = tab['75%'] - tab['25%']
    tab = tab[ ['mean', '50%', 'IQR']]
    p = pd.read_csv('experiments.csv', index_col=0)
    p_list = ['Normalisation', 'Channels', 'Learning_rate']


    c_pos_list_1 = [-0.15 * (i+1)  for i in range(tab.shape[1])][::-1]
    c_pos_list_2 = [-0.2 * (i) + min(c_pos_list_1)-0.15 for i in range(3)]


    for c_label, c_pos in zip(tab.columns,
                            c_pos_list_1):

        plt.text(c_pos, -0.65, c_label, fontsize=10, fontweight='bold', va='center')

        for r_pos, r_label in enumerate(tab.index):
            plt.text(c_pos, r_pos,
                    '{:.2f}'.format(tab[c_label][ r_label]),
                        va='center', fontsize=10)

            for t, p_t in zip(p_list, c_pos_list_2[::-1]):
                s = p[t][ '_'.join(r_label.split('_')[:2])]
                if t=='Learning_rate':
                    s = '{:.0e}'.format(s)
                else:
                    s= s.replace('Z-Score', 'ZS').replace(' ','')

                plt.text(p_t, r_pos,
                         s,
                        fontsize=10, va='center')



def fig_comb_folds(data, data_folds):
    tab = {}

    marker_folds = ['v', '<', '^', '>', 'D']

    fig, ax =  plt.subplots(1,1, figsize=(10,10))


    for p in [0.2, 0.4, .6, .8, .1,.3, .5, .7, .9]:
        plt.axvline(p, alpha=0.1, color='k')

    for ((key, value), p) in zip(data.items(), range(11)):
        col = ('#78c679' if p < 8 else '#ff8c00')
        box_violin(value['f1_score'].tolist(), [p], col, ax)


        # add indicators for individual folds
        for idx, p_sub, m in zip(key.split('_')[1:], [-0.2, -0.1, 0,  .1, .2], marker_folds):

            # plt.plot(data_folds['bigart_'+idx]['f1_score'].mean(), p+p_sub,
            #         marker = m, color='k', zorder=1000, markersize=3,
            #         fillstyle='none' )
            plt.plot(data_folds['bigart_'+idx]['f1_score'].median(), p+p_sub,
                    marker = m, color='k', zorder=1000, markersize=3)


        tab[key] =list(value.describe()['f1_score'])



    plt.ylim( 8.5, -0.5)
    plt.xlim(0,1)
    plt.yticks(range(11), ['']*11)
    plt.xlabel('DSC$_{P}$')

    tab = pd.DataFrame().from_dict(tab, orient='index',
            columns= ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])


    add_table(ax, tab)


def part_1():
    src = r'D:\BiGART_results'
    data = get_data(src)
    data_combined_folds = combine_folds(data)

    fig_comb_folds(data_combined_folds, data)
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.savefig('Fig2.pdf')

part_1()
