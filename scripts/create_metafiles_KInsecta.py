"""Create metafiles for image and wingbeat data for KInsecta"""

import sys
# Insert libraries paths from 1 on; 0 is the script path
sys.path.insert(1, '../beexplainable')

import glob
import numpy as np
from beexplainable.utils import metafile_readers as mr

# Metafile folder
bees_folder  = "../metafiles/KInsecta/"
subfolder    = "all_data/"

# Root path
BEES_PATH = '../../../data/KInsecta_SPIE/' + subfolder

# Read class names
CLASSES_PATH = bees_folder + subfolder + "classes.txt"
cls_dict = mr.metafile_to_dict(CLASSES_PATH)

images_train = open(bees_folder + subfolder + "images_train.txt", "a")
image_class_labels_train = open(bees_folder + subfolder + "image_class_labels_train.txt", "a")
wingbeats_train = open(bees_folder + subfolder + "wingbeats_train.txt", "a")
wing_class_labels_train = open(bees_folder + subfolder + "wing_class_labels_train.txt", "a")
images_test = open(bees_folder + subfolder + "images_test.txt", "a")
image_class_labels_test = open(bees_folder + subfolder + "image_class_labels_test.txt", "a")
wingbeats_test = open(bees_folder + subfolder + "wingbeats_test.txt", "a")
wing_class_labels_test = open(bees_folder + subfolder + "wing_class_labels_test.txt", "a")

# Create metafiles for all images and wingbeats
total_img_ind, total_wng_ind = 1, 1 # indexes for all the files (incremented continually and starts at 1 as in CUB)
for c in cls_dict.values():

    img_ind, wng_ind = 0, 0  # indexes for current species (always reset)

    # Get class index from its name
    cls_ind = list(cls_dict.keys())[list(cls_dict.values()).index(c)]

    # Note: only store every 3rd image path. For every sample, 3 frames of the same 2-second-video were stored;
    # when the insect does not move, all 3 frames are the same
    img_paths = glob.glob(BEES_PATH + c + '/*/*/images/*.png')[::3]
    wng_paths = glob.glob(BEES_PATH + c + '/*/*/wingbeats/*.wav')

    # Split into training and test
    # For every species, look whether there are more images or wingbeats available.
    # Take 1/3 of the minimum count and choose randomly paths for the test set.
    min_len = min(len(img_paths), len(wng_paths))
    test_len = min_len // 3

    # Shuffle both lists of paths
    np.random.shuffle(img_paths)
    np.random.shuffle(wng_paths)

    # Iterate over image paths
    for im in img_paths:

        # Get file name in form class_name/num_frames/time_stamp/images/image_name.png
        file_name = im[ im.find(c) : ]

        # Store first test_len shuffled paths as test files, all the others as train
        if img_ind < test_len:
            images_test.write(str(total_img_ind) + ' ' + file_name + '\n')
            image_class_labels_test.write(str(total_img_ind) + ' ' + str(cls_ind) + '\n')
        else:
            images_train.write(str(total_img_ind) + ' ' + file_name + '\n')
            image_class_labels_train.write(str(total_img_ind) + ' ' + str(cls_ind) + '\n')

        img_ind += 1
        total_img_ind += 1

    # Iterate over wingbeat paths
    for wb in wng_paths:

        # Get file name in form class_name/num_frames/time_stamp/wingbeats/wingbeat_name.wav
        file_name = wb[wb.find(c):]

        # Store first test_len shuffled paths as test files, all the others as train
        if wng_ind < test_len:
            wingbeats_test.write(str(total_wng_ind) + ' ' + file_name + '\n')
            wing_class_labels_test.write(str(total_wng_ind) + ' ' + str(cls_ind) + '\n')
        else:
            wingbeats_train.write(str(total_wng_ind) + ' ' + file_name + '\n')
            wing_class_labels_train.write(str(total_wng_ind) + ' ' + str(cls_ind) + '\n')

        wng_ind += 1
        total_wng_ind += 1

    print(c + ' done.')

images_train.close(); images_test.close();
image_class_labels_train.close(); image_class_labels_test.close();
wingbeats_train.close(); wingbeats_test.close();
wing_class_labels_train.close(); wing_class_labels_test.close()