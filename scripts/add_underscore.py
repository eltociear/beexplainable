"""Rename a subfolder name from 'Genus species' to 'Genus_species'"""

import os, glob

BEES_PATH = '../../../data/KInsecta_SPIE/wingbeats_listhof_alt/'
subfolds = glob.glob(BEES_PATH + '*')

for subfold in subfolds:
    os.chdir(subfold)
    curr_files = os.listdir()

    for f in curr_files:
        f_new = f.replace(' ', '_')
        os.rename(f, f_new)
    os.chdir('..')