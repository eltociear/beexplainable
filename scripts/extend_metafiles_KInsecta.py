"""Extend training metafiles with extra wingbeats"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob
from beexplainable.utils import metafile_readers as mr

# Metafile folder
bees_folder  = "../metafiles/KInsecta/"
subfolder    = "all_data/"

# Root path
BEES_PATH = '../../../data/KInsecta_SPIE/wingbeats_listhof_alt/'

# Reopen training metafiles
wingbeats_train = open(bees_folder + subfolder + "wingbeats_train_2.txt", "a")
wing_class_labels_train = open(bees_folder + subfolder + "wing_class_labels_train_2.txt", "a")

# Read all class names
CLASSES_PATH = bees_folder + subfolder + "classes.txt"
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

# Read class names to extend (not all classes have extra wavs)
cls_subfolders = glob.glob(BEES_PATH + '*')
cls_to_extend  = [c.split('/')[-1] for c in cls_subfolders]

# Extend metafiles with new wingbeats
total_wng_ind = 1 # indexes for all the files (incremented continually and starts at 1 as in CUB)
for c in cls_to_extend:
    # Get class index from its name
    cls_ind = list(cls_dict.keys())[list(cls_dict.values()).index(c)]

    # Read wav-paths for current species
    wng_paths = glob.glob(BEES_PATH + c + '/*.wav')

    # Iterate over wingbeat paths
    for wb in wng_paths:

        # Get file name in form class_name/wingbeat_name.wav
        file_name = wb[wb.find(c):]

        # Store paths as train files
        wingbeats_train.write(str(total_wng_ind) + ' ' + file_name + '\n')
        wing_class_labels_train.write(str(total_wng_ind) + ' ' + str(cls_ind) + '\n')
        total_wng_ind += 1

    print(c + ' done.')

wingbeats_train.close()
wing_class_labels_train.close()