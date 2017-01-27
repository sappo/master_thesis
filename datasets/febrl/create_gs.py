import pandas as pd
import re
df = pd.read_csv("ferbl-90k-10k-1.csv")
rec_col = df.rec_id

duplicates = {}
pattern = re.compile("(^.*)dup")
for id in rec_col:
    m = pattern.match(id)
    if m:
        org_id = m.group(1) + "org"
        if not org_id in  duplicates.keys():
            duplicates[org_id] = []

        duplicates[org_id].append(id)

print(duplicates)
print(len(duplicates))

target = open("./ferbl-90k-10k-1_gold.csv", 'w')
target.write("org_id")
target.write(", ")
target.write("dup_id")
target.write("\n")
for org_id in duplicates.keys():
    for dup_id in duplicates[org_id]:
        target.write(org_id)
        target.write(", ")
        target.write(dup_id)
        target.write("\n")

target.close()
