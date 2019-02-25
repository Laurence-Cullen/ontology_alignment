import numpy as np
import pandas
from sklearn import metrics
from vec_builder import load_hpo_terms, build_hpo_snomed_map, build_snomed_hpo_map


def load_vec_file(path):
    return pandas.read_csv(
        path,
        sep=' ',
        index_col=0,
        header=None
    )


def main():
    hpo_vectors = load_vec_file('vectors/hpo_name_bert_vanilla_uncased_large.vec')
    snomed_vectors = load_vec_file('vectors/snomed_name_bert_vanilla_uncased_large.vec')

    # print(hpo_vectors.to_numpy())
    # print(snomed_vectors)

    pairwise_distances = metrics.pairwise.cosine_similarity(
        X=snomed_vectors.to_numpy(copy=True),
        Y=hpo_vectors.to_numpy(copy=True)
    )

    hpo_terms = load_hpo_terms()
    hpo_snomed_map = build_hpo_snomed_map(hpo_terms)
    snomed_hpo_terms = build_snomed_hpo_map(hpo_snomed_map)

    print(pairwise_distances.shape)

    top_similarities_to_check = 10

    # snomed_to_similar_hpo_terms = {}

    for i in range(pairwise_distances.shape[0]):
        max_indices = np.argpartition(pairwise_distances[i, :], -top_similarities_to_check)[-top_similarities_to_check:]


    # print(max_indices)
    # print(pairwise_distances[0, :][max_indices])


if __name__ == '__main__':
    main()
