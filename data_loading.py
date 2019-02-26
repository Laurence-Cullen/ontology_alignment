import contextlib
import re

import pandas
import pronto

hpo_terms_file = 'ontologies/hp.obo'
snomed_terms_file = 'ontologies/snomed_terms.tab'

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


def load_snomed_terms():
    snomed_terms_df = pandas.read_csv(snomed_terms_file, sep='\t')

    snomed_terms = {}
    for row in snomed_terms_df.itertuples():
        snomed_terms[int(getattr(row, 'db_id'))] = getattr(row, 'name')

    return snomed_terms


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
