import pronto
import contextlib


def load_hpo_terms():
    hpo = pronto.Ontology('data/hp.obo')
    max_hpo_id = 3000079

    terms = {}
    for hpo_id in range(0, max_hpo_id + 1):
        with contextlib.suppress(KeyError):
            terms[hpo_id] = hpo[f"HP:{hpo_id:07d}"]

    return terms


def build_vec_file(hpo_terms):
    pass

def main():
    hpo_terms = load_hpo_terms()
    print(hpo_terms)


if __name__ == '__main__':
    main()
