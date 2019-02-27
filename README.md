# ontology_alignment
Experiments aligning HPO and SNOMED medical ontologies

GPU machine IP: 86.17.97.132

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

## Fine tune model
Third experiment is to see if fine tuning the BERT model on pubmed
or another large medical text corpus improves the power of the sentence
embeddings. Fine tuning will need to be done on a cloud TPU due to time
and memory constraints.

Corpus to fine tune on acquired from the [PMC open access archives](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
