#!/usr/bin/env python2

# This script will extract regional voxel counts for a set of thresholded statistical maps

import imageutils as utils
import glob

# STOPPED HERE - do this for a smaller matrix! (aka, make function to resample image to smaller, hen do)
files = glob.glob("/home/vanessa/Documents/Work/BRAINBEHAVIOR/mrs/*.nii.gz")
standard = "data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz"

df = utils.normalize(files,standard)
