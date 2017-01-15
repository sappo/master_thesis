import os
from collections import defaultdict
import pyprind
import subprocess
import pandas as pd

columns = ["name_prefix","first_name","middle_name","last_name","name_suffix","age","gender","race","ethnic","street_address","city","state","zip_code","full_phone_num","birth_place","register_date","download_month"]


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

bar = pyprind.ProgBar(file_len("ncvoter-20140619-temporal.csv"), monitor=True)

if os.path.exists("ncvoter.csv"):
    os.remove("ncvoter.csv")
if os.path.exists("ncvoter_gold.csv"):
    os.remove("ncvoter_gold.csv")

csv_chunks = pd.read_csv("./ncvoter-20140619-temporal.csv",
                  iterator=True, chunksize=10000,
                  error_bad_lines=False,
                  index_col=False,
                  dtype='unicode',
                  encoding = "ISO-8859-1")

print("Read chunks")
# Get ids
print_header = True
id_col = defaultdict(list)
for chunk in csv_chunks:
    for index, id in zip(chunk.index, chunk.loc[:, ('voter_id')].values):
        id_col[id].append(index)

    chunk.to_csv("ncvoter.csv", mode="a", chunksize=10000,
                 header=print_header, index_label="id",
                 columns=columns, encoding="ISO-8859-1")

    print_header = False
    bar.update(9999)

print("ids found", len(id_col))

target = open("./ncvoter_gold.csv", 'w')
target.write("id_1")
target.write(",")
target.write("id_2")
target.write("\n")
for id in id_col.keys():
    if len(id_col[id]) > 1:
        index = 0
        # Move over array to generate all pairs
        while len(id_col[id][index + 1:]) > 0:
            for candidate in id_col[id][index + 1:]:
                target.write("%s,%s\n" % (id_col[id][index], candidate))
            index += 1

target.close()
