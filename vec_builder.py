import contextlib

from bert_serving.client import BertClient

from data_loading import load_hpo_terms, load_snomed_terms, build_snomed_hpo_map, build_hpo_snomed_map

# connecting to remote bert server
bc = BertClient(ip='86.17.97.132')  # ip address of the GPU machine

hpo_terms_file = 'ontologies/hp.obo'
snomed_terms_file = 'ontologies/snomed_terms.tab'


def build_vec_file(terms_list, save_path):
    names = [terms_list[i][1] for i in range(len(terms_list))]

    print(names)

    vectors = bc.encode(names)
    print('got vectors')

    with open(save_path, 'w+') as file:
        for i in range(len(terms_list)):

            if i % 100 == 0:
                print(f'processed {i} terms')

            vector = list(vectors[i].flatten().astype(dtype=str))

            file.write(str(terms_list[i][0]) + ' ' + ' '.join(vector) + '\n')


def build_hpo_vectors():
    hpo_terms = load_hpo_terms()
    hpo_terms_list = [[hpo_id, hpo_term.name] for hpo_id, hpo_term in hpo_terms.items()]
    build_vec_file(terms_list=hpo_terms_list, save_path='hpo.vec')


def build_snomed_vectors():
    hpo_terms = load_hpo_terms()
    print('hpo terms loaded')

    snomed_terms = load_snomed_terms()
    print('snomed terms loaded')

    hpo_snomed_map = build_hpo_snomed_map(hpo_terms)
    snomed_hpo_map = build_snomed_hpo_map(hpo_snomed_map)
    print('built snomed -> hpo terms map')

    filtered_snomed_terms = {}
    for snomed_id, _ in snomed_hpo_map.items():
        with contextlib.suppress(KeyError):
            filtered_snomed_terms[snomed_id] = snomed_terms[int(snomed_id)]
    print('extracted subset of snomed names for terms referenced in hpo')

    snomed_terms_list = [[snomed_id, snomed_name] for snomed_id, snomed_name in filtered_snomed_terms.items()]
    build_vec_file(terms_list=snomed_terms_list, save_path='snomed.vec')


def main():
    build_snomed_vectors()


if __name__ == '__main__':
    main()
