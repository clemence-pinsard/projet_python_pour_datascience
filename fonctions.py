import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors


def calc_ratio_d10(group):
    """
    Calcule le ratio du taux de chaque décile par rapport au 10ème décile.
    """
    # On s'assure que valGroupage est bien comparé à un entier 10
    d10_val = group.loc[group['valGroupage'].astype(int) == 10, 'txStandDir'].values
    if len(d10_val) > 0:
        group['ratio_to_D10'] = group['txStandDir'] / d10_val[0]
    else:
        group['ratio_to_D10'] = np.nan
    return group


def calc_ratio_dip(group):
    # La modalité 4 correspond à l'enseignement supérieur
    ref_val = group.loc[group['valGroupage'] == 4, 'txStandDir'].values
    if len(ref_val) > 0:
        group['ratio_to_Sup'] = group['txStandDir'] / ref_val[0]
    else:
        group['ratio_to_Sup'] = np.nan
    return group


def plot_bivariate_metropole(geodf, var1, var2, label_x, label_y):
    # 1. Filtrage pour ne garder que la Métropole
    # On exclut les codes régions de l'Outre-mer (971, 972, 973, 974, 976)
    codes_drom = ['01', '02', '03', '04', '06', '971', '972', '973', '974', '976']
    geodf_metropole = geodf[~geodf['code'].isin(codes_drom)].copy()

    pathologies = geodf_metropole['catLib'].unique()

    # Paramètres de la grille
    n_cols = 2
    n_rows = (len(pathologies) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 8 * n_rows))
    axes = axes.flatten()

    bi_colors = [
        "#e8e8e8", "#b0d5df", "#64acbe", # y=0 (Bas)
        "#e4acac", "#ad9ea5", "#627f8c", # y=1 (Moyen)
        "#c85a5a", "#985356", "#574249"  # y=2 (Haut)
    ]
    cmap_bi = mcolors.ListedColormap(bi_colors)

    for i, patho in enumerate(pathologies):
        ax = axes[i]
        temp_df = geodf_metropole[geodf_metropole['catLib'] == patho].copy()

        if len(temp_df) < 3:
            ax.axis('off')
            continue

        # Calcul des terciles
        temp_df['x_cat'] = pd.qcut(temp_df[var1].rank(method='first'), 3, labels=[0, 1, 2])
        temp_df['y_cat'] = pd.qcut(temp_df[var2].rank(method='first'), 3, labels=[0, 1, 2])
        temp_df['bi_class'] = temp_df['x_cat'].astype(int) + temp_df['y_cat'].astype(int) * 3

        # Tracé de la carte
        temp_df.plot(column='bi_class', cmap=cmap_bi, ax=ax, edgecolor='black', linewidth=0.3)
        ax.set_title(patho, fontsize=14, fontweight='bold')
        ax.axis('off')

        # Légende miniature
        ax_leg = ax.inset_axes([0.80, 0.1, 0.15, 0.15]) 
        for y in range(3):
            for x in range(3):
                ax_leg.add_patch(plt.Rectangle((x, y), 1, 1, color=bi_colors[x + y*3]))

        ax_leg.set_xlim(0, 3); ax_leg.set_ylim(0, 3)
        ax_leg.set_xticks([0.5, 2.5]); ax_leg.set_yticks([0.5, 2.5])
        ax_leg.set_xticklabels(['-', '+'], fontsize=7)
        ax_leg.set_yticklabels(['-', '+'], fontsize=7)
        ax_leg.set_xlabel(label_x, fontsize=7)
        ax_leg.set_ylabel(label_y, fontsize=7)

    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.suptitle(f"Analyse Bivariée (France Métropolitaine) : {label_x} vs {label_y}",
                 fontsize=20, y=1.01)
    plt.tight_layout()
    plt.show()
