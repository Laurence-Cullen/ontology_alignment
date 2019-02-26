import pathlib
import contextlib


def build_corpus(target_dir, corpus_save_path):
    paper_paths = pathlib.Path(target_dir).glob('**/*')

    files_written = 0

    with open(corpus_save_path, 'w+') as corpus_file:
        for paper_path in paper_paths:
            if paper_path.is_dir() or '.DS_Store' in str(paper_path):
                continue

            if files_written % 1000 == 0:
                print(f'{files_written} files written')

            with paper_path.open() as paper_file:
                with contextlib.suppress(UnicodeDecodeError):
                    for line in paper_file.readlines():
                        if '==== Refs' in line:
                            break
                        elif '====' in line:
                            continue
                        elif len(line) < 3:
                            corpus_file.write('\n')
                        else:
                            sentences = [sentence.strip(' \t\n\r') + '.\n' for sentence in line.split('.')]
                            for sentence in sentences:
                                if len(sentence) > 2:
                                    corpus_file.write(sentence)

            files_written += 1


def main():
    target_dir = 'medical_corpuses/comm'
    corpus_path = 'comm_corpus.txt'

    build_corpus(target_dir=target_dir, corpus_save_path=corpus_path)


if __name__ == '__main__':
    main()
