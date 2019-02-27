import numpy as np
import pandas
import contextlib
from sklearn import metrics

from data_loading import load_hpo_terms, build_snomed_hpo_map, build_hpo_snomed_map, load_rich_snomed_terms, \
    load_rich_hpo_terms, load_snomed_terms


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

    rich_hpo_terms = load_rich_hpo_terms()
    print(rich_hpo_terms)
    rich_hpo_terms = {element[0]: element[1] for element in rich_hpo_terms}


    snomed_terms = load_snomed_terms()

    filtered_snomed_terms = {}
    for snomed_id, _ in snomed_hpo_map.items():
        with contextlib.suppress(KeyError):
            filtered_snomed_terms[snomed_id] = snomed_terms[int(snomed_id)]
    print('extracted subset of snomed names for terms referenced in hpo')

    rich_snomed_terms = load_rich_snomed_terms(filtered_snomed_terms)
    rich_snomed_terms = {element[0]: element[1] for element in rich_snomed_terms}

    print(pairwise_distances.shape)

    top_similarities_to_check = 1

    # {snomed_id: [1, 2, 3, etc]} maps from snomed id to list of hpo terms with strong cosine similarity
    snomed_to_similar_hpo_terms = {}

    hbo_indices = hpo_vectors.index.values
    snomed_indices = snomed_vectors.index.values

    correct_matches = 0

    for i in range(pairwise_distances.shape[0]):
        max_indices = np.argpartition(pairwise_distances[i, :], -top_similarities_to_check)[-top_similarities_to_check:]

        snomed_code = snomed_indices[i]
        similar_hpo_codes = hbo_indices[max_indices]

        if int(snomed_hpo_map[str(snomed_code)]) in list(similar_hpo_codes):
            print('Successful match!')
            print(f'SNOMED {snomed_code}:', rich_snomed_terms[str(snomed_code)])
            print(f'HPO {similar_hpo_codes[0]}:', rich_hpo_terms[f"{similar_hpo_codes[0]:07d}"], '\n')
            correct_matches += 1
        else:
            print('Failed match...')
            print(f'SNOMED {snomed_code}:', rich_snomed_terms[str(snomed_code)])
            print(f'most similar HPO {similar_hpo_codes[0]}:', rich_hpo_terms[f"{similar_hpo_codes[0]:07d}"])
            print(f'actual HPO {snomed_hpo_map[str(snomed_code)]}:', rich_hpo_terms[f"{snomed_hpo_map[str(snomed_code)]:07d}"], '\n')

        snomed_to_similar_hpo_terms[snomed_code] = similar_hpo_codes

    print(f'top {top_similarities_to_check} similar hpo terms included the correct'
          f' term {100 * correct_matches / len(snomed_indices):.2f}% of the time')


def main():
    score_vector_pair(
        hpo_vec_path='vectors/hpo_rich_bert_vanilla_uncased_large.vec',
        snomed_vec_path='vectors/snomed_rich_bert_vanilla_uncased_large.vec'
    )


if __name__ == '__main__':
    main()
