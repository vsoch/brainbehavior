#!/usr/bin/env python2

# This script will parse CNP data, and do simple clustering with question labels mapped on
# (aka, early exploration of data)

from brainbehavior.wkpedia import get_page_content, get_headers, get_section_text
from brainbehavior.nlp import get_term_counts
import pandas
import pickle

# Step 1: Get counts for behavioral terms list
output_folder = "/home/vanessa/Documents/Dropbox/Website/traits/data"
terms = pickle.load(open("%s/behavior_list.pkl" %(output_folder),"rb"))
test_disorder = "major depressive disorder"
text = get_page_content(test_disorder)
headers = get_headers(text)
sections = headers[0:2] # [u'== Symptoms and signs ==', u'=== Comorbidity ===']
section_text = get_section_text(text,sections)
counts = get_term_counts(terms=terms,text=section_text)

#TODO: Talk to Russ/Chris about how to derive features for ontology
# We can count frequencies of terms in different documents
# For simple example I will define a "feature" of depression as having a coun
# of the term in the wikipedia definition.

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import re

# Step 2: Parse CNP data
data1 = pandas.read_csv("analysis/data/HTAC_Qry_Custom_1.csv",low_memory=False)
data2 = pandas.read_csv("analysis/data/HTAC_Qry_Custom_2.csv",low_memory=False)
data = pandas.DataFrame.merge(data1,data2,on="ptid")
data.index = data.ptid
data = data.loc[data.ptid.isnull()==False]
#data.to_pickle("analysis/data/CNP_raw.pkl")

# The variables that are skipped are in experimentname, sessiondate, sessiontime
# mr_time, scid, spanlanguage

# And we want to skip these
testdate = re.compile("testdate")
initials = re.compile("initials")
with PdfPages('analysis/data/cnp_plots.pdf') as pdf:
    for v in range(1,len(data.columns)):
        variable = data.columns[v]
        # Skip over testdates and initials
        if not testdate.search(variable) and not initials.search(variable):
            try:
                plt.figure(figsize=(3,3));
                missing = data[variable][data[variable].isnull()].shape[0]
                defined = data[variable][data[variable].isnull()==False]
                plt.title("%s (nan=%s)" %(variable,missing))
                data[variable].plot(kind='hist', alpha=0.5)
                pdf.savefig()
                plt.close()
            except:
                print variable
                plt.close()


# TODO: Ask Russ about data privacy, add data to CogatPheno database (remove from repo?)
# Then write functions to explore interactively

# Read in data export
from brainbehavior.cognitiveatlas import read_cogpheno
import numpy as np
cogpheno = read_cogpheno()

# Index with lowercase version
lower_labels = [x.lower() for x in cogpheno["question_label"]]
cogpheno.index = lower_labels

# Subset data to those that we have defined in cogatpheno
overlap_labels = [x for x in lower_labels if x in data.columns]
cogatpheno_subset = data[overlap_labels]
#cogatpheno_subset.to_pickle("analysis/data/CNP_cogatpheno.pkl")

# Try multidimensional scaling for a first go
cap_defined = cogatpheno_subset.copy()

from matplotlib.collections import LineCollection
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA

# Fill in missing values with mean (bad practice, but will do for first try)
for variable in cap_defined.columns:
    tmp = cap_defined[variable]
    meta = cogpheno.loc[variable]
    # Rough estimation if is binary [0,1]
    if 0 in tmp.unique() and 1 in tmp.unique():
        majority = tmp.value_counts().index[tmp.value_counts()==tmp.value_counts().max()][0]
        tmp[tmp.isnull()] = majority
    else:
        tmp[tmp.isnull()] = tmp.mean()
    # Now center (mean zero)
    tmp -= tmp.mean()    
    cap_defined[variable] = tmp

# Find if there are any infinite - we want to remove!
for variable in cap_defined.columns:
    tmp = cap_defined[variable]
    if not np.isfinite(tmp).all():
        cap_defined = cap_defined.drop(variable,1)
# assessqsymptom
# assessqdisorder

# Calculate euclidean distances
similarities = euclidean_distances(cap_defined)
mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(similarities).embedding_
nmds = manifold.MDS(n_components=2, metric=False, max_iter=3000, eps=1e-12,
                    dissimilarity="precomputed", n_jobs=1,n_init=1)
npos = nmds.fit_transform(similarities, init=pos)

# Rescale the data STOPPED HERE
X_true = cap_defined.copy()
pos *= np.sqrt((X_true ** 2).sum()) / np.sqrt((pos ** 2).sum())
npos *= np.sqrt((X_true ** 2).sum()) / np.sqrt((npos ** 2).sum())

# Rotate the data
clf = PCA(n_components=2)
X_true = clf.fit_transform(X_true)
pos = clf.fit_transform(pos)
npos = clf.fit_transform(npos)

fig = plt.figure(1)
ax = plt.axes([0., 0., 1., 1.])
plt.scatter(X_true[:, 0], X_true[:, 1], c='r', s=20)
plt.scatter(pos[:, 0], pos[:, 1], s=20, c='g')
plt.scatter(npos[:, 0], npos[:, 1], s=20, c='b')
plt.legend(('True position', 'MDS', 'NMDS'), loc='best')

similarities = similarities.max() / similarities * 100
similarities[np.isinf(similarities)] = 0

# Plot the edges
start_idx, end_idx = np.where(pos)
#a sequence of (*line0*, *line1*, *line2*), where::
#            linen = (x0, y0), (x1, y1), ... (xm, ym)
segments = [[X_true[i, :], X_true[j, :]]
            for i in range(len(pos)) for j in range(len(pos))]
values = np.abs(similarities)
lc = LineCollection(segments,
                    zorder=0, cmap=plt.cm.hot_r,
                    norm=plt.Normalize(0, values.max()))
lc.set_array(similarities.flatten())
lc.set_linewidths(0.5 * np.ones(len(segments)))
ax.add_collection(lc)

plt.show()

