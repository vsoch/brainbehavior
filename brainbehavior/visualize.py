#!/usr/bin/env python

"""

visualize: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

import numpy as np
import pylab as plt
from nilearn.plotting.img_plotting import plot_anat
from neurosynth.base.dataset import Dataset
from neurosynth.analysis import meta
import matplotlib.pyplot as plt
import brewer2mpl
import matplotlib.gridspec as gridspec
import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as sch

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"


"""Save png file for a single image"""
def plot_mr(input_mr,output_png):
  display = plot_anat(standard,display_mode='z',cut_coords=np.linspace(-30, 60, 7))
  display.add_overlay(newimage, vmin=0,cmap=plt.cm.hot, colorbar=True)
  display._colorbar_ax.set_yticklabels(["% 3i" % (100 * float(t.get_text())) for t in display._colorbar_ax.yaxis.get_ticklabels()])
  display.title("Vanessa's First Plot in Nilearn!'")
  display.savefig(output_png)

"""Generate a heatmap from a data frame"""
def heatmap(data_frame,output_image):
  #TODO: Vanessa does not know how to plot properly, need to learn!
  # Remove regions with no voxels of activation
  activated_regions = data_frame.ix[:,data_frame.columns[data_frame.index[data_frame.mean(axis=0) != 0]]]
  pairwise_dists = distance.squareform(distance.pdist(activated_regions))
  clusters = sch.linkage(pairwise_dists,method='complete')
  den = sch.dendrogram(clusters)
  heatmap = activated_regions.ix[den['leaves']]
  plt.pcolor(heatmap)
  plt.savefig('/home/vanessa/Desktop/foo.png', bbox_inches='tight')

"""Generate a plot to show voxel count distributions for each atlas"""
def feature_plots(data_frame,output_image):
  # First let's do hierarchical clustering!

