#!/usr/bin/env python

"""

utils: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that 
combined can make inferences about disorders and behaviors:

NeuroVault: functional and structural group analyses
Cognitive Atlas: ontology of cognitive concepts, tasks, disorder, collections
NeuroSynth: mining literature for behavioral concepts to produce brain maps

SAMPLE USAGE: Please see README included with package


"""

import json

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/07/24 $"
__license__ = "Python"


"""Save json to file"""
def save_json(myjson,output_file):
    filey = open(output_file,"wb")    
    myjson = json.dumps(myjson, sort_keys=True, indent=4, separators=(',', ': '))
    filey.writelines(myjson)
    filey.close()

"""Read in a formatted file with group names and PMID assignments: each line has
a group name followed by a single list of PMIDs - one group per line.  Returns
a lookup dictionary of group"""
def read_pmid_groups(input_file,separator="\t"):
  filey = open(input_file,"r")
  groups = dict()
  for f in filey.readlines():
    group = f.strip("\n").split("\t")
    name = group.pop(0)
    group = [g.strip(" ") for g in group]
    groups[name] = group
  filey.close()
  return groups

