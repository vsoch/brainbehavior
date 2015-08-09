#!/usr/bin/env python2
# We want to know, of the files we have, what is the breakdown?

from brainbehavior.cognitiveatlas import behaviors_to_pickle, load_behaviors

# default is to generate expanded list to brainbehavior/data/cognitiveatlas/behavioraltraits.pkl
behaviors_to_pickle()

# Load behaviors
traits = load_behaviors()


