# SNOMED to HPO Ontology alignment
Experiments aligning HPO and SNOMED medical ontologies to be able to map
from SNOMED terms to the HPO term which best matches it.

## Background
[SNOMED](https://termbrowser.nhs.uk/?) is a large medical ontology for
general medical use that can verge into the sprawling with a very large
number of terms and quite a lot of repetition. For genetic disease
community the alternative HPO ontology has become popular, it is tightly
maintained and tries to stay minimalistic and focused on 

## Motivation
In NLP systems attempting to draw insights from medical records, such as extracting
a set of symptoms, may be focused on a particular ontology. However, seeing as there
are a variety of ontologies in common use systems can be made more powerful and general
if they are able to include information from multiple ontologies.

Between ontologies there are some explicit mappings of terms but only in the minority
of cases. Therefore, it is useful to build a system which is able to automatically
account for cases without explicit term linking.

## Resources
I will be using the recently released BERT sentence embedding model from Google
to encode the names, synonyms and descriptions of terms to vectors of the
same length.

[BERT GitHub](https://github.com/google-research/bert)

For ease of use in getting vectors from new sentences I will be using BERT
as a service which came out of Tencent AI Labs and makes it super easy
to deploy BERT locally and remotely. In my case I was working on the train
but my laptop does not have a GPU so I set up my home PC as a BERT server
so I could hit it every time I wanted to get a sentence vectorised.

[BERT as a service](https://github.com/hanxiao/bert-as-service)

To fine tune the BERT model I am attempting to use a full text archive
of PubMed from their [open access portal](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
as a training corpus.


## Naive attempt
Using the large, uncased english BERT model without fine tuning
to create sentence embeddings from just the names of both
SNOMED and and HPO terms.

First attempt at mapping SNOMED to HPO terms managed 
to get the correct HPO term in the top 10 most cosine similar
terms 35.7% of the time.

## Averaging vectors for synonyms
Second experiment is to see if averaging sentence embeddings
of the name, description and synonyms of terms creates stronger link.

In a first experiment in this strand only the HPO term vectors were
created from averaged vectors of name, description and synonyms.
When now compared to the name based SNOMED vectors the top 10 score
rose to 50.7%.

After building rich SNOMED vectors and comparing them to the original
name based HPO vectors a top 10 accuracy of 63.6% is achieved.

Now, combing rich embeddings of HPO and SNOMED terms a top 10 similarity
score of 79.5% is achieved. When looking only at the top 3 most similar
HPO terms to a SNOMED term the accuracy only falls to 71.27%. 58.4% of the
time the most similar HPO term is correct.

Other ideas to try in this vein include averaging in vectors of parent categories
or building multiple vectors for each HPO and SNOMED term including embeddings
of the parent classes of the respective terms to include more information
about the hierarchy of terms.

Seeing as SNOMED terms can often be degenerate it could be useful to average
hierarchy embedding of all degenerate terms to create a wider view of the context
of a term.

## Fine tune model
Third experiment is to see if fine tuning the BERT model on pubmed
or another large medical text corpus improves the power of the sentence
embeddings. Fine tuning will need to be done on a cloud TPU due to time
and memory constraints.

Corpus to fine tune on acquired from the [PMC open access archives](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
