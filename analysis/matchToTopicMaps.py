#!/usr/bin/env python2

# This script will test matching the images in the NeuroSynth database to topic maps

import imageutils as utils
import glob
from imageutils import correlation
import pandas as pd

# STEP 1: Extract matrix of normalized values in 8mm voxel space for 2D visualization ----------
standard = "/home/vanessa/Documents/Dropbox/Code/Python/BrainBehavior/brainbehavior/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz"
standard8mm = utils.resize_image(standard,[8,8,8])

# Now let's get the NeuroSynth topic maps
topic_maps = pd.read_csv("data/topicmaps/topicMapsLookup.csv",sep="\t")
topic_maps_directory = "/home/vanessa/Documents/Work/NEUROSYNTH/topicmaps/maps/"
topic_map_files = [ topic_maps_directory + "topic" +  str(x) + "_pAgF_z_FDR_0.05.nii.gz" for x in list(topic_maps.image_label) ]
topic_map_data = utils.files_get_3d_list(topic_map_files)

# Prepare some better labels
labels = list(topic_maps.topic_label)

# Normalize the topic maps into the standard 8mm space.  They are already Z scores.
matrix = utils.spatial_normalize_images(topic_map_data,standard8mm)
matrix.columns = labels

# This will be 16128 voxels (rows) and 80 images

# Now let's get our neurovault images, and put them in the same space, and convert all to Z scores
nv_maps = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs/*.nii")
nv_maps = utils.files_get_3d_list(nv_maps)
nv_matrix = utils.spatial_normalize_images(nv_maps,standard8mm,zscore=True)
# This will also be 16128 voxels and 383 images

# Next, we want to know how similar each neurovault map is to the topic maps.  We can use the utils.correlation function
corr = correlation(nv_matrix,matrix)

# We can now save to file
corr.to_csv("data/nv2nsy_pearson.tsv",sep="\t")
