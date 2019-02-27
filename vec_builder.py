import contextlib

import numpy
from bert_serving.client import BertClient

import data_loading

# connecting to remote bert server
# bc = BertClient(ip='86.17.97.132')  # ip address of the GPU machine
bc = BertClient(ip='192.168.0.34')  # local ip address of the GPU machine

hpo_terms_file = 'ontologies/hp.obo'
snomed_terms_file = 'ontologies/snomed_terms.tab'

embedding_dims = 1024


def build_vec_file(terms_list, save_path):
    descriptions = [terms_list[i][1] for i in range(len(terms_list))]

    print(descriptions)

    vectors = numpy.zeros(shape=(len(terms_list), embedding_dims), dtype=float)

    counter = 0
    for i in range(len(terms_list)):
        if counter % 100 == 0:
            print(f'{counter} terms encoded')

        if isinstance(descriptions[i], list):
            vectors[i] = numpy.mean(bc.encode(descriptions[i]), axis=0)
        else:
            vectors[i] = bc.encode(descriptions[i])

        counter += 1

    print('got vectors')

    with open(save_path, 'w+') as file:
        for i in range(len(terms_list)):

            vector = list(vectors[i].flatten().astype(dtype=str))

            file.write(str(terms_list[i][0]) + ' ' + ' '.join(vector) + '\n')


def build_hpo_vectors(rich=False):
    if rich:
        hpo_terms_list = data_loading.load_rich_hpo_terms()

    else:
        hpo_terms = data_loading.load_hpo_terms()
        hpo_terms_list = [[hpo_id, hpo_term.name] for hpo_id, hpo_term in hpo_terms.items()]

    build_vec_file(terms_list=hpo_terms_list, save_path='hpo.vec')


def build_snomed_vectors(rich=False):
    hpo_terms = data_loading.load_hpo_terms()
    print('hpo terms loaded')

    snomed_terms = data_loading.load_snomed_terms()
    print('snomed terms loaded')

    hpo_snomed_map = data_loading.build_hpo_snomed_map(hpo_terms)
    snomed_hpo_map = data_loading.build_snomed_hpo_map(hpo_snomed_map)
    print('built snomed -> hpo terms map')

    filtered_snomed_terms = {}
    for snomed_id, _ in snomed_hpo_map.items():
        with contextlib.suppress(KeyError):
            filtered_snomed_terms[snomed_id] = snomed_terms[int(snomed_id)]
    print('extracted subset of snomed names for terms referenced in hpo')

    if rich:
        snomed_terms_list = data_loading.load_rich_snomed_terms(filtered_snomed_terms)
        print(snomed_terms_list)
    else:
        snomed_terms_list = [[snomed_id, snomed_name] for snomed_id, snomed_name in filtered_snomed_terms.items()]

    build_vec_file(terms_list=snomed_terms_list, save_path='snomed.vec')


def main():
    build_snomed_vectors(rich=True)
    build_hpo_vectors(rich=True)


if __name__ == '__main__':
    main()
