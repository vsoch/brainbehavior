brainbehavior
============

Extract behavioral trait associations from relevant literature to derive a cognitive phenotype to relate to brain imaging.

### The Plan

1. Start with my terms
2. Use word net to get synonyms ("is_a"), either for parents ("hypernyms") or children ("hyponyms"). We should go all the way up the tree to "entity."
3. We might also want to get opposites (some thesaurus?)
4. Create database of terms, and visualize ontology
5. Parse some corpus, and break into papers about disorders that we have in RDoC, cognitive atlas, and behavioral data.
6. For each term in ontology, take simple counts to calculate the probability of the term given the disorder. (or probabiliy of term1 given term2 in title (meaning the literature is "about" that term))
7. We may want to do something more intelligent like parsing individual sentences and breaking into parts of speech, determining some kind of more detailed relationship about terms (other than co-occurence). Will determine this when I get there.
8. Finished ontology should be explorable in web interface, define how behavioral traits are related (definition wise), and how they are related in the literature (based on disorders). We can then extend to actual behavioral data.
