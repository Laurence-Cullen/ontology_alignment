from sklearn import metrics
import pandas


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

    print(pairwise_distances.shape)


if __name__ == '__main__':
    main()
