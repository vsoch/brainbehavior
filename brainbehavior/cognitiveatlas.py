#!/usr/bin/env python

"""

CognitiveAtlas: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that
combined can make inferences about disorders and behaviors:

SAMPLE USAGE: Please see README included with package


"""

from textblob import Word
from textblob.wordnet import Synset
import pickle
import numpy
import pandas
import json

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2015/07/24 $"
__license__ = "Python"

# Cognitive Atlas Functions---------------------------------------------------------

"""Read in file of local disorders to create pickle object
THIS WILL BE UPDATED TO USE COGNITIVE ATLAS PYTHON API WRAPPER
"""
def read_local_disorders(self):
    import pickle
    filey = open("data/disorder_subset_10-31-14.csv","r")
    disorders = filey.readlines()
    filey.close()
    header = disorders.pop(0).strip("\n").strip("\r").strip(" ").split(",")
    disorder = dict()
    for d in disorders:
        tmp = d.strip("\n").strip("\r").strip("'").strip('"').split("\t")
        did = tmp.pop(0).strip('"')
        # Here are the search terms
        labels = tmp[2].strip('"')
        disorder[did] = labels
    # Save to pickle object
    pickle.dump(disorder, open( "data/CAdisorders.pkl", "wb" ) )

def load_disorders(self):
    import pickle
    return pickle.load( open( "data/CAdisorders.pkl", "rb" ) )

# Behaviors --------------------------------------------------------------------
class Behavior:

    def __init__(self,trait):
        self.get_trait(trait)
        self.is_a = self.get_synonyms()
        self.specifier = ''

    def get_trait(self,trait):
        self.trait = trait.split("(")[0].strip()
        if len(trait.split("(")) > 1:
            self.specifier = trait.split("(")[1].replace(")","").strip()

    def __str__(self):
        return self.trait

    def __repr__(self):
        return self.trait

    def get_synonyms(self):
        word = Word(self.trait)
        self.definitions = word.definitions
        return word.synsets

    def get_json(self,sim_metric="path"):
        # First make list of all unique synsets
        synsets = get_behavior_synset(self)
        return get_behavior_json(synsets,sim_metric=sim_metric)
        

# Global functions
def make_node(syn,nid,class_name):
    return {"name":syn.name(),
            "nid":nid,
            "class":class_name,
            "definition":syn.definition(),
            "example":"|".join([x for x in syn.examples()]),
            "lexname":syn.lexname(),
            "lemmanames":"|".join([x for x in syn.lemma_names()]),
            "pos":syn.pos(),
            "similartos":"|".join([x.name() for x in syn.similar_tos()]),
            "topicdomains":"|".join([x.name() for x in syn.topic_domains()])}

def get_json(behaviors,sim_metric="path"):
    synsets = get_behaviors_synsets(behaviors)
    return get_behavior_json(synsets,sim_metric)

'''Get path distance for each of syn1 and syn2'''
def get_relation(syn1,syn2,sim_metric):
    from nltk.corpus import wordnet as wn
    if sim_metric == "path":
        # https://stackoverflow.com/questions/20075335/is-wordnet-path-similarity-commutative
        sim_score = min(wn.path_similarity(syn1,syn2), wn.path_similarity(syn2,syn1))
    elif sim_metric == "lch":
        if syn1.pos() == syn2.pos():
            sim_score = syn1.lch_similarity(syn2)
        else:
            sim_score = 0
    elif sim_metric == "wup":
        sim_score = syn1.wup_similarity(syn2)
    if sim_score: return sim_score
    else: return 0 
    

'''Return link json for two nodes'''
def make_link(syn1,syn2,sim,sim_metric):
    nid1 = syn1["nid"]
    nid2 = syn2["nid"]
    return {"source":nid1,"target":nid2,"value":sim,"metric":sim_metric}

# Extract a list of all synsets, lemmas, and "similartos"
def get_term_objects(behaviors):
    synsets = get_behaviors_synsets(behaviors)
    all_terms = []
    for syn,data in synsets.iteritems(): # synsets already contain parents/child etc.
        # We also need to get the lemmas
        lemmas = data["data"].lemmas()
        lemma_synsets = [l.synset() for l in lemmas]
        new_terms = [data["data"]] + data["data"].similar_tos() + lemma_synsets
        all_terms = all_terms + new_terms
    return all_terms

# Extract family from a synset
def get_synset_family(synset):
    lemmas = [l.synset() for l in synset.lemmas()]
    family = numpy.unique(synset.similar_tos() + lemmas).tolist()
    return family

# Get unique strings to parse text (we can compare Word strings and text blobs)
def get_term_strings(behaviors,word_only=True):
    all_terms = get_term_objects(behaviors)
    # Now we want a string associated with each
    term_strings = []
    for term in all_terms:
        if word_only:
            term_strings.append(term.name().split(".")[0])
        else:
            term_strings.append(term.name())
    term_strings = numpy.unique(term_strings).tolist()
    # Finally, some terms don't have synsets, add them
    for behavior in behaviors:
        if behavior.trait not in term_strings:
            term_strings.append(behavior.trait) 
    return numpy.sort(term_strings).tolist()

# Generate a matrix of path similarity scores between all terms, for use in text parsing
# Synset selection is a dictionary of chosen synsets, one for each term
def get_path_similarity_matrix(behaviors,synset_selection,sim_metric="path"):
    from nltk.corpus.reader.wordnet import Lemma, Synset as Syn

    # First we need a list of all lemmas (similarity == 1) and relevant synsets
    term_objects = []

    for b in range(0,len(behaviors)):
        behavior = behaviors[b] 
 
        # If we even have synsets or lemmas
        if len(behavior.is_a) > 0:
            # If the term has a matching synset
            if isinstance(synset_selection[behavior.trait],str):
                correct_synset = Synset(synset_selection[behavior.trait])
                term_objects.append(correct_synset)

                # Filter synset to the one we are interested in
                family = get_synset_family(correct_synset)
                term_objects = term_objects + family 
            
        # If not, append the name of the term
        else:
            term_objects.append(behavior.trait)

    # Now we will fill in the data frame with similarities
    names = []
    for obj in term_objects:
        if isinstance(obj,str):
            names.append(obj)
        else:
            names.append(obj.name())
    names = numpy.unique(names).tolist()
    df = pandas.DataFrame(columns=names,index=names)

    # Now calculate similarities
    strings = numpy.unique([s for s in term_objects if isinstance(s,str)]).tolist()
    syns = numpy.unique([s for s in term_objects if isinstance(s,Syn)]).tolist()

    # First calculate for synsets
    for t1 in range(0,len(syns)):
        term1 = syns[t1]
        term1_name = term1.name()
        df.loc[term1_name,term1_name] = 1
        print "Calculating path similarity for term %s, %s of %s" %(term1_name,t1,len(syns))
        for t2 in range(0,len(syns)):
            if t1 < t2:
                term2 = syns[t2]
                term2_name = term2.name()
                sim_score = get_relation(term1,term2,sim_metric)
                df.loc[term1_name,term2_name] = sim_score
                df.loc[term2_name,term1_name] = sim_score

    # Now fill in 0 for behaviors not in wordNet (they are in their own family)    
    for s in range(0,len(strings)):
        string = strings[s]
        df.loc[string] = 0
        df[string] = 0
        df.loc[string,string] = 1

    return df


def get_behavior_json(synsets,sim_metric="path"):
    if sim_metric in ["path","lch","wup"]:
        
        # We need to define the similarity (links) between all synsets
        links = []
        for s1 in range(len(synsets.keys())):
            for s2 in range(len(synsets.keys())):
                if s1<s2:
                    syn1 = synsets.keys()[s1]
                    syn2 = synsets.keys()[s2]
                    sim = get_relation(synsets[syn1]["data"],synsets[syn2]["data"],sim_metric=sim_metric)
                    if sim != None:
                        links.append(make_link(synsets[syn1],synsets[syn2],sim,sim_metric))

        # Extract nodes from the synsets
        nodes = []
        for syn in synsets.keys():
            nodes.append(synsets[syn]["node"])
        return {"links":links,"nodes":nodes}

    else:
        print "Error: sim_metric must be one of 'path'\n'lch':semantic relatedness of word senses using the method described by Leacock and Chodorow (1998) or \n'wup': semantic relatedness of word senses using the edge counting method of the of Wu & Palmer (1994)"
 

def get_behaviors_synsets(behaviors):
    synsets = dict()
    all_nids = []
    if not isinstance(behaviors,list):
        behaviors = [behaviors]
    nid = 1
    for behavior in behaviors:
        new_synsets = get_behavior_synset(behavior,nid)
        new_nids = [new_synsets[x]["nid"] for x in new_synsets.keys()]
        all_nids = all_nids + new_nids
        nid = numpy.max(all_nids) + 1
        synsets.update(new_synsets)
    return synsets


def get_behavior_synset(behavior,nid=1):
    synsets = dict()
    for s in range(len(behavior.is_a)):
        syn = behavior.is_a[s]
        node = make_node(syn,nid,behavior.trait)
        # We will only include relationships that are descriptors
        acceptable_pos = ["s","a"]
        synsets[syn.name()] = {"data":syn,"nid":nid,"node":node}
        nid = nid + 1
        # parents and children
        relations = syn.hypernyms() + syn.hyponyms()
        while relations:
            relation = relations.pop()
            if relation.pos() in acceptable_pos:
                node = make_node(relation,nid,behavior.trait)
                synsets[relation.name()] = {"data":relation,"nid":nid,"node":node}
                nid = nid + 1
                new_relations = [new for new in relation.hypernyms() + relation.hyponyms() if new.name() not in synsets.keys()]
                relations = relations + new_relations
    return synsets

def read_cogpheno(input_file="brainbehavior/data/cognitiveatlas/cogPheno_782.tsv"):
    return pandas.read_csv(input_file,sep="\t")

def save_behaviors(input_file="brainbehavior/data/cognitiveatlas/cogPheno_782.tsv",
                  output_file="brainbehavior/data/cognitiveatlas/behavioraltraits.pkl"):
    cogpheno = read_cogpheno(input_file)
    traits = cogpheno.question_behavioral_trait.unique()
    traits.sort()
    traits = traits.tolist()[1:len(traits)]
    traits = [x for x in traits if x not in ["nan","None"]]
    pickle.dump(traits,open(output_file,"wb"))

def load_behaviors(input_pickle="brainbehavior/data/cognitiveatlas/behavioraltraits.pkl"):
    return pickle.load(open(input_pickle,"rb"))
