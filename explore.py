import contextlib
import sys

import pronto
# on another CPU machine
from bert_serving.client import BertClient

# connecting to remote bert server
bc = BertClient(ip='86.17.97.132')  # ip address of the GPU machine

hpo_terms_file = 'ontologies/hp.obo'


def load_hpo_term_names():
    hpo = pronto.Ontology(hpo_terms_file)
    max_hpo_id = 3000079

    terms = {}
    for hpo_id in range(0, max_hpo_id + 1):
        with contextlib.suppress(KeyError):
            terms[hpo_id] = hpo[f"HP:{hpo_id:07d}"]

    return terms


def build_vec_file(hpo_terms, save_path):
    hpo_terms_list = [[hpo_id, hpo_term.name] for hpo_id, hpo_term in hpo_terms.items()]
    names = [hpo_terms_list[i][1] for i in range(len(hpo_terms_list))]

    print(names)

    vectors = bc.encode(names)
    print('got vectors')

    with open(save_path, 'w+') as file:
        for i in range(len(hpo_terms_list)):

            if i % 100 == 0:
                print(f'processed {i} terms')

            vector = list(vectors[i].flatten().astype(dtype=str))

            file.write(str(hpo_terms_list[i][0]) + ' ' + ' '.join(vector) + '\n')


def main():
    hpo_terms = load_hpo_term_names()

    build_vec_file(hpo_terms=hpo_terms, save_path='hpo.vec')


if __name__ == '__main__':
    main()
