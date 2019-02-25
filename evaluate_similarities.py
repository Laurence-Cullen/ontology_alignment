import sklearn

pairwise_distances = sklearn.metrics.pairwise.cosine_similarity(X=snomed_vectors, Y=hpo_vectors)