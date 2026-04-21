import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


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
    """
    Calcule le ratio du taux de chaque niveau de diplôme par rapport au
    niveau 'Enseignement supérieur' (modalité 4), pris comme référence.
    Un ratio > 1 indique un taux plus élevé que chez les plus diplômés.
    Retourne NaN si la modalité de référence est absente du groupe.
    """
    # La modalité 4 correspond à l'enseignement supérieur
    ref_val = group.loc[group['valGroupage'] == 4, 'txStandDir'].values
    if len(ref_val) > 0:
        group['ratio_to_Sup'] = group['txStandDir'] / ref_val[0]
    else:
        group['ratio_to_Sup'] = np.nan
    return group


def plot_bivariate(geodf, var1, var2, label_x, label_y):
    """
    Trace une carte bivariée (grille 3×3 de terciles) pour chaque catégorie
    de pathologie présente dans geodf, en croisant var1 (axe X) et var2 (axe Y).

    Paramètres
    ----------
    geodf    : GeoDataFrame avec une colonne 'catLib' pour itérer par pathologie.
    var1     : colonne affectée à l'axe horizontal (ex. 'D1').
    var2     : colonne affectée à l'axe vertical (ex. 'ratio_D1_D10').
    label_x  : étiquette X de la légende (ex. 'Prév. (D1)').
    label_y  : étiquette Y de la légende (ex. 'Inégalité').
    """

    pathologies = geodf['catLib'].unique()

    n_cols = 2
    n_rows = (len(pathologies) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 8 * n_rows))
    axes = axes.flatten()

    bi_colors = [
        "#e8e8e8", "#b0d5df", "#64acbe",
        "#e4acac", "#ad9ea5", "#627f8c",
        "#c85a5a", "#985356", "#574249"
    ]
    cmap_bi = mcolors.ListedColormap(bi_colors)

    for i, patho in enumerate(pathologies):
        ax = axes[i]
        temp_df = geodf[geodf['catLib'] == patho].copy()

        if len(temp_df) < 3:
            ax.axis('off')
            continue

        temp_df['x_cat'] = pd.qcut(temp_df[var1].rank(method='first'), 3, labels=[0, 1, 2])
        temp_df['y_cat'] = pd.qcut(temp_df[var2].rank(method='first'), 3, labels=[0, 1, 2])
        temp_df['bi_class'] = temp_df['x_cat'].astype(int) + temp_df['y_cat'].astype(int) * 3

        temp_df.plot(column='bi_class', cmap=cmap_bi, ax=ax, edgecolor='black', linewidth=0.3)

        titre = patho if len(patho) <= 35 else patho[:33] + '…'
        ax.set_title(titre, fontsize=11, fontweight='bold')
        ax.axis('off')

        ax_leg = ax.inset_axes([0.80, 0.05, 0.15, 0.15])
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

    plt.suptitle(f"Analyse Bivariée (France entière) : {label_x} vs {label_y}",
                 fontsize=20, y=1.01)
    plt.tight_layout()
    plt.show()


def plot_cartes_regions(map_data, colonne, titre, cmap='YlOrRd', fmt=None):
    """
    Trace une série de cartes choroplèthes régionales, une par catégorie de
    pathologie présente dans map_data.

    Paramètres
    ----------
    map_data : GeoDataFrame avec une colonne 'catLib' et la colonne à cartographier.
    colonne  : str — nom de la colonne à représenter (ex. 'ratio_D1_D10', 'taux_pct').
    titre    : str — titre global de la figure.
    cmap     : str — palette de couleurs matplotlib (défaut 'YlOrRd').
    fmt      : str ou None — format de la colorbar (ex. '%.1f%%'). None = défaut.
    """
    pathologies = map_data['catLib'].unique()
    n_cols = 4
    n_rows = (len(pathologies) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten()

    legend_kwds = {'shrink': 0.8}
    if fmt:
        legend_kwds['format'] = fmt

    for i, patho in enumerate(pathologies):
        ax = axes[i]
        data_patho = map_data[map_data['catLib'] == patho].copy()
        data_patho.plot(column=colonne, ax=ax, legend=True,
                        cmap=cmap, edgecolor='black', linewidth=0.5,
                        legend_kwds=legend_kwds)
        ax.set_title(patho, fontsize=10)
        ax.axis('off')

    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.suptitle(titre, fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()


def choisir_k_optimal(matrice_scaled, k_min=2, k_max=10):
    """
    Affiche la méthode du coude et le score de silhouette pour choisir k dans
    un clustering K-Means, et retourne le k qui maximise le score de silhouette.

    Paramètres
    ----------
    matrice_scaled : array-like — données normalisées à clusteriser.
    k_min, k_max   : int — plage de valeurs de k à tester (bornes incluses).

    Retourne
    --------
    k_optimal : int — valeur de k maximisant le score de silhouette.
    """
    K = range(k_min, k_max + 1)
    inerties, silhouettes = [], []

    for k in K:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(matrice_scaled)
        inerties.append(km.inertia_)
        silhouettes.append(silhouette_score(matrice_scaled, labels))

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))

    axes[0].plot(K, inerties, marker='o', color='steelblue')
    axes[0].set_xlabel("Nombre de clusters (k)")
    axes[0].set_ylabel("Inertie")
    axes[0].set_title("Méthode du coude")

    axes[1].plot(K, silhouettes, marker='o', color='darkorange')
    axes[1].set_xlabel("Nombre de clusters (k)")
    axes[1].set_ylabel("Score de silhouette")
    axes[1].set_title("Score de silhouette selon k")

    plt.tight_layout()
    plt.show()

    k_optimal = list(K)[silhouettes.index(max(silhouettes))]
    print(f"Score de silhouette maximal : {max(silhouettes):.3f} → k optimal = {k_optimal}")
    return k_optimal
