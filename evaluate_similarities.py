import numpy as np
import pandas
from sklearn import metrics

from data_loading import load_hpo_terms, build_snomed_hpo_map, build_hpo_snomed_map


def load_vec_file(path):
    return pandas.read_csv(
        path,
        sep=' ',
        index_col=0,
        header=None
    )


def score_vector_pair(hpo_vec_path, snomed_vec_path):

    hpo_vectors = load_vec_file(hpo_vec_path)
    snomed_vectors = load_vec_file(snomed_vec_path)

    # print(hpo_vectors.to_numpy())
    # print(snomed_vectors)

    pairwise_distances = metrics.pairwise.cosine_similarity(
        X=snomed_vectors.to_numpy(copy=True),
        Y=hpo_vectors.to_numpy(copy=True)
    )

    hpo_terms = load_hpo_terms()
    hpo_snomed_map = build_hpo_snomed_map(hpo_terms)
    snomed_hpo_map = build_snomed_hpo_map(hpo_snomed_map)

    print(pairwise_distances.shape)

    top_similarities_to_check = 10

    # {snomed_id: [1, 2, 3, etc]} maps from snomed id to list of hpo terms with strong cosine similarity
    snomed_to_similar_hpo_terms = {}

    hbo_indices = hpo_vectors.index.values
    snomed_indices = snomed_vectors.index.values

    correct_matches = 0

    for i in range(pairwise_distances.shape[0]):
        max_indices = np.argpartition(pairwise_distances[i, :], -top_similarities_to_check)[-top_similarities_to_check:]

        snomed_code = snomed_indices[i]
        similar_hpo_codes = hbo_indices[max_indices]

        # print('actual hpo code', snomed_hpo_map[str(snomed_code)])
        # print('similar hpo codes', list(similar_hpo_codes))

        if int(snomed_hpo_map[str(snomed_code)]) in list(similar_hpo_codes):
            correct_matches += 1

        snomed_to_similar_hpo_terms[snomed_code] = similar_hpo_codes

    print(f'top {top_similarities_to_check} similar hpo terms included the correct'
          f' term {100 * correct_matches / len(snomed_indices):.2f}% of the time')


def main():
    score_vector_pair(
        hpo_vec_path='vectors/hpo_name_bert_vanilla_uncased_large.vec',
        snomed_vec_path='vectors/snomed_name_bert_vanilla_uncased_large.vec'
    )


if __name__ == '__main__':
    main()
