import os
import subprocess
import click
import pyprind
from collections import defaultdict
import pandas as pd


def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.argument('ground_truth')
@click.argument('dataset')
@click.option(u'-e', u'--encoding', default="utf-8")
def main(ground_truth, dataset, encoding):
    progress_bar = pyprind.ProgBar(file_len(dataset), monitor=True, update_interval=1)

    index_filename = os.path.splitext(os.path.basename(dataset))[0] + "_index.csv"
    train_filename = os.path.splitext(os.path.basename(dataset))[0] + "_train.csv"
    train_query_filename = os.path.splitext(os.path.basename(dataset))[0] + "_train_query.csv"
    train_gt_filename = os.path.splitext(os.path.basename(dataset))[0] + "_train_gold.csv"
    validate_filename = os.path.splitext(os.path.basename(dataset))[0] + "_validate.csv"
    validate_query_filename = os.path.splitext(os.path.basename(dataset))[0] + "_validate_query.csv"
    validate_gt_filename = os.path.splitext(os.path.basename(dataset))[0] + "_validate_gold.csv"
    test_filename = os.path.splitext(os.path.basename(dataset))[0] + "_test.csv"
    test_query_filename = os.path.splitext(os.path.basename(dataset))[0] + "_test_query.csv"
    test_gt_filename = os.path.splitext(os.path.basename(dataset))[0] + "_test_gold.csv"

    if os.path.exists(index_filename):
        os.remove(index_filename)
    if os.path.exists(train_filename):
        os.remove(train_filename)
    if os.path.exists(train_query_filename):
        os.remove(train_query_filename)
    if os.path.exists(train_gt_filename):
        os.remove(train_gt_filename)
    if os.path.exists(validate_filename):
        os.remove(validate_filename)
    if os.path.exists(validate_query_filename):
        os.remove(validate_query_filename)
    if os.path.exists(validate_gt_filename):
        os.remove(validate_gt_filename)
    if os.path.exists(test_filename):
        os.remove(test_filename)
    if os.path.exists(test_query_filename):
        os.remove(test_query_filename)
    if os.path.exists(test_gt_filename):
        os.remove(test_gt_filename)

    ground_truth_chunks = pd.read_csv(ground_truth,
                                      iterator=True,
                                      chunksize=10000,
                                      skipinitialspace=True,
                                      error_bad_lines=False,
                                      index_col=False,
                                      dtype='unicode',
                                      encoding = encoding)

    db_duplicates = set()
    query_duplicates = set()
    db_lookup = defaultdict(list)
    query_lookup = defaultdict(list)
    for chunk in ground_truth_chunks:
        for id_1, id_2 in chunk.loc[:, ('id_1', 'id_2')].values:
            id_1 = strip(id_1)
            id_2 = strip(id_2)
            db_duplicates.add(id_1)
            query_duplicates.add(id_2)

            db_lookup[id_1].append(id_2)

        progress_bar.update(0, item_id="Reading ground truth")

    duplicate_intersection = db_duplicates.intersection(query_duplicates)
    db_duplicates = db_duplicates.difference(duplicate_intersection)
    for duplicate in duplicate_intersection:
        db_lookup.pop(duplicate)

    round_robin = 0
    for key in db_lookup.keys():
        if len(db_lookup[key]) > 1:
            for index, q_id in enumerate(db_lookup[key]):
                query_lookup[q_id] = round_robin % 3
                round_robin += 1

    progress_bar.update(0, item_id="Reading dataset")
    dataset_chunks = pd.read_csv(dataset,
                                 iterator=True,
                                 chunksize=10000,
                                 skipinitialspace=True,
                                 error_bad_lines=False,
                                 index_col=False,
                                 dtype='unicode',
                                 encoding = encoding)

    print_header = True
    round_robin_select = 0
    round_robin_duplicates = 0
    round_robin_none_duplicates = 0
    index_record_ids = set()
    train_record_ids = set()
    validate_record_ids = set()
    test_record_ids = set()
    for chunk in dataset_chunks:
        index = []
        train = []
        validate = []
        test = []
        for record in chunk.values:
            if record[0] in db_duplicates:
                index.append(record)
                index_record_ids.add(record[0])
            elif record[0] in query_duplicates:
                if record[0] in query_lookup:
                    round_robin_select = query_lookup[record[0]]
                else:
                    round_robin_select = round_robin_duplicates
                    round_robin_duplicates += 1
                    round_robin_duplicates %= 3

                if round_robin_select == 0:
                    train.append(record)
                    train_record_ids.add(record[0])
                elif round_robin_select == 1:
                    validate.append(record)
                    validate_record_ids.add(record[0])
                elif round_robin_select == 2:
                    test.append(record)
                    test_record_ids.add(record[0])

            else:
                if round_robin_none_duplicates > 2:
                    index.append(record)
                    index_record_ids.add(record[0])
                elif round_robin_none_duplicates == 0:
                    train.append(record)
                    train_record_ids.add(record[0])
                elif round_robin_none_duplicates == 1:
                    validate.append(record)
                    validate_record_ids.add(record[0])
                elif round_robin_none_duplicates == 2:
                    test.append(record)
                    test_record_ids.add(record[0])

                round_robin_none_duplicates += 1
                round_robin_none_duplicates %= 6

        db_df = pd.DataFrame(index, columns=chunk.columns)
        db_df.to_csv(index_filename, index=False,
                     mode="a", chunksize=10000,
                     encoding="utf-8", header=print_header)

        train_df = pd.DataFrame(train, columns=chunk.columns)
        train_df.to_csv(train_query_filename, index=False,
                        mode="a", chunksize=10000,
                        encoding="utf-8", header=print_header)

        validate_df = pd.DataFrame(validate, columns=chunk.columns)
        validate_df.to_csv(validate_query_filename, index=False,
                           mode="a", chunksize=10000,
                           encoding="utf-8", header=print_header)

        test_df = pd.DataFrame(test, columns=chunk.columns)
        test_df.to_csv(test_query_filename, index=False,
                       mode="a", chunksize=10000,
                       encoding="utf-8", header=print_header)

        del db_df
        del train_df
        del validate_df
        del test_df
        del index
        del train
        del validate
        del test
        print_header = False
        progress_bar.update(len(chunk), item_id="Splitting dataset")
        del chunk

    ground_truth_chunks = pd.read_csv(ground_truth,
                                      iterator=True,
                                      chunksize=10000,
                                      skipinitialspace=True,
                                      error_bad_lines=False,
                                      index_col=False,
                                      dtype='unicode',
                                      encoding = encoding)

    train_gold = []
    validate_gold = []
    test_gold = []
    for chunk in ground_truth_chunks:
        for id_1, id_2 in chunk.loc[:, ('id_1', 'id_2')].values:
            id_1 = strip(id_1)
            id_2 = strip(id_2)
            if id_1 in index_record_ids and id_2 in train_record_ids:
                train_gold.append([id_1, id_2])
            if id_1 in index_record_ids and id_2 in validate_record_ids:
                validate_gold.append([id_1, id_2])
            if id_1 in index_record_ids and id_2 in test_record_ids:
                test_gold.append([id_1, id_2])

        progress_bar.update(0, item_id="Calculating split ground truth")

    train_gold_df = pd.DataFrame(train_gold, columns=['id_1', 'id_2'])
    train_gold_df.to_csv(train_gt_filename, index=False,
                         mode="a", chunksize=10000, encoding="utf-8")

    validate_gold_df = pd.DataFrame(validate_gold, columns=['id_1', 'id_2'])
    validate_gold_df.to_csv(validate_gt_filename, index=False,
                            mode="a", chunksize=10000, encoding="utf-8")

    test_gold_df = pd.DataFrame(test_gold, columns=['id_1', 'id_2'])
    test_gold_df.to_csv(test_gt_filename, index=False,
                        mode="a", chunksize=10000, encoding="utf-8")

    with open(train_filename, 'w') as outfile:
        with open(index_filename) as index_file:
            for line in index_file:
                outfile.write(line)
        with open(train_query_filename) as query_file:
            # Discard header line
            next(query_file)
            for line in query_file:
                outfile.write(line)

    with open(validate_filename, 'w') as outfile:
        with open(index_filename) as index_file:
            for line in index_file:
                outfile.write(line)
        with open(validate_query_filename) as query_file:
            # Discard header line
            next(query_file)
            for line in query_file:
                outfile.write(line)

    with open(test_filename, 'w') as outfile:
        with open(index_filename) as index_file:
            for line in index_file:
                outfile.write(line)
        with open(test_query_filename) as query_file:
            # Discard header line
            next(query_file)
            for line in query_file:
                outfile.write(line)

    print()

if __name__ == "__main__":  # pragma: no cover
        main(prog_name="dataset splitter")
