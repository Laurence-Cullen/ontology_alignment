# ontology_alignment
Experiments aligning HPO and SNOMED medical ontologies

GPU machine IP: 86.17.97.132


## Naive attempt
Using the large, uncased english BERT model without fine tuning
to create sentence embeddings from just the names of both
snomed and and hpo terms.

First attempt at mapping snomed to hpo terms managed 
to get the correct hpo term in the top 10 most cosine similar
terms 35.7% of the time.

## Averaging vectors for synonyms
Second experiment is to see if averaging sentence embeddings
of the name, description and synonyms of terms creates stronger link.


## Fine tune model
Third experiment is to see if fine tuning the BERT model on pubmed
or another large medical text corpus improves the power of the sentence
embeddings. Fine tuning will need to be done a cloud TPU due to time
and memory constraints.