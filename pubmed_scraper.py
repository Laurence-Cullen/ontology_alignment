import requests
import pandas

# base_url = 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/'
# open_access_list_path = 'oa_file_list.txt'

bulk_files_base = 'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/'

bulk_files = [
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/comm_use.0-9A-B.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/comm_use.C-H.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/comm_use.I-N.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/comm_use.O-Z.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.0-9A-B.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.C-H.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.I-N.txt.tar.gz',
    'ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/non_comm_use.O-Z.txt.tar.gz'
]


def main():
    pass


if __name__ == '__main__':
    main()
