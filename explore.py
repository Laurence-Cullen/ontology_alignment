import contextlib
import re

import pandas
import pronto
# on another CPU machine
from bert_serving.client import BertClient

# connecting to remote bert server
bc = BertClient(ip='86.17.97.132')  # ip address of the GPU machine

hpo_terms_file = 'ontologies/hp.obo'
snomed_terms_file = 'ontologies/snomed_terms.tab'

# re to extract snomed IDs from obo serialisations of HPO terms
snomed_id_finder = r'SNOMEDCT_US:(\d*)(?:\n|$)'


def load_hpo_term():
    hpo = pronto.Ontology(hpo_terms_file)
    max_hpo_id = 3000079

    terms = {}
    for hpo_id in range(0, max_hpo_id + 1):
        with contextlib.suppress(KeyError):
            terms[hpo_id] = hpo[f"HP:{hpo_id:07d}"]

    return terms


def load_snomed_terms():
    snomed_terms_df = pandas.read_csv(snomed_terms_file, sep='\t')

    snomed_terms = {}
    for row in snomed_terms_df.itertuples():
        snomed_terms[int(getattr(row, 'db_id'))] = getattr(row, 'name')

    return snomed_terms


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
    hpo_terms = load_hpo_term()
    snomed_terms = load_snomed_terms()

    hpo_to_snomed_matches = {}

    for hpo_id, term in hpo_terms.items():
        serialised_term = term.obo

        match = re.search(snomed_id_finder, serialised_term)
        if match:
            hpo_to_snomed_matches
            print(match.group(1))


    # build_vec_file(hpo_terms=hpo_terms, save_path='hpo.vec')


if __name__ == '__main__':
    main()
