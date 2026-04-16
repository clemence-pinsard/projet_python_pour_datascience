import numpy as np

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