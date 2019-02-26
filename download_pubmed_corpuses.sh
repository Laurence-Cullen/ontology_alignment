#!/usr/bin/env bash

BASE_URL="ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/"
EXTENSION=".txt.tar.gz"
SAVE_DIR="medical_corpuses/"

declare -a archives=(
    "comm_use.0-9A-B"
    "comm_use.C-H"
    "comm_use.O-Z"
    "non_comm_use.0-9A-B"
    "non_comm_use.C-H"
    "non_comm_use.I-N"
    "non_comm_use.O-Z"
)

for archive in "${archives[@]}"
do
    wget ${BASE_URL}${archive}${EXTENSION}
    tar xvzf ${archive}${EXTENSION} "${SAVE_DIR}${archive}"
    rm ${archive}${EXTENSION}
done
