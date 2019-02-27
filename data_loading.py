import contextlib
import re

import pandas
import pronto

hpo_terms_file = 'ontologies/hp.obo'
snomed_terms_file = 'ontologies/snomed_terms.tab'
snomed_synonyms_file = 'ontologies/snomed_synonyms.tab'

# re to extract snomed IDs from obo serialisations of HPO terms
snomed_id_finder = r'SNOMEDCT_US:(\d*)(?:\n|$)'


def load_hpo_terms():
    hpo = pronto.Ontology(hpo_terms_file)
    max_hpo_id = 3000079

    terms = {}
    for hpo_id in range(0, max_hpo_id + 1):
        with contextlib.suppress(KeyError):
            terms[f"{hpo_id:07d}"] = hpo[f"HP:{hpo_id:07d}"]

    return terms


def load_rich_hpo_terms():
    hpo_terms = load_hpo_terms()

    hpo_terms_list = []
    for hpo_id, hpo_term in hpo_terms.items():
        descriptions = [hpo_term.name]

        # add def field if present in term
        if hpo_term.desc:
            descriptions.append(str(hpo_term.desc))

        # add all listed synonyms
        for synonym in hpo_term.synonyms:
            descriptions.append(synonym.desc)

        hpo_terms_list.append([hpo_id, descriptions])

    return hpo_terms_list


def load_snomed_terms():
    snomed_terms_df = pandas.read_csv(snomed_terms_file, sep='\t')

    snomed_terms = {}
    for row in snomed_terms_df.itertuples():
        snomed_terms[int(getattr(row, 'db_id'))] = getattr(row, 'name')

    return snomed_terms


def load_rich_snomed_terms(snomed_terms):
    snomed_synonyms = pandas.read_csv(snomed_synonyms_file, sep='\t')

    snomed_terms_list = []
    for db_id, name in snomed_terms.items():
        descriptions = [name]
        # print(db_id)

        for synonym_row in snomed_synonyms.loc[snomed_synonyms['db_to_id'] == int(db_id)].itertuples():
            # print(synonym_row)
            # print(db_id)
            # print(getattr(synonym_row, 'name'))
            descriptions.append(getattr(synonym_row, 'name'))

        snomed_terms_list.append([db_id, descriptions])

    return snomed_terms_list


def build_hpo_snomed_map(hpo_terms):
    hpo_to_snomed_matches = {}

    for hpo_id, term in hpo_terms.items():
        serialised_term = term.obo

        # search for SNOMED xrefs
        match = re.search(snomed_id_finder, serialised_term)
        while match:
            if hpo_id in hpo_to_snomed_matches:
                hpo_to_snomed_matches[hpo_id].append(match.group(1))
            else:
                hpo_to_snomed_matches[hpo_id] = [match.group(1)]

            # slicing out match
            serialised_term = serialised_term[:match.span()[0]] + serialised_term[match.span()[1]:]

            # looking for new match
            match = re.search(snomed_id_finder, serialised_term)

    return hpo_to_snomed_matches


def build_snomed_hpo_map(hpo_snomed_map):
    snomed_hpo_map = {}
    for hpo_id, snomed_ids in hpo_snomed_map.items():
        for snomed_id in snomed_ids:
            snomed_hpo_map[snomed_id] = hpo_id

    return snomed_hpo_map


def main():
    snomed_synonyms = pandas.read_csv(snomed_synonyms_file, sep='\t')

    # print(snomed_synonyms)

    db_id = 82525005

    # print(snomed_synonyms.loc[snomed_synonyms['db_to_id'] == db_id])

    for synonym_row in snomed_synonyms.loc[snomed_synonyms['db_to_id'] == db_id].itertuples():
        print(synonym_row)
        # print(db_id)
        # descriptions.append(synonym_row['name'])


if __name__ == '__main__':
    main()
