# Dynamic similarity-aware inverted indexing for real-time entity resolution
This paper improves the Similarity-Aware Inverted Index approach from
[@CG:Scalable:08] to allows dynamic additions to the index. Also it investigates
the frequency-distribution of data and the effect of reducing the index to hold
only frequent records. In recent years dynamic entity resolution becomes more
and more important as many businesses used databases that are not static and
change over time. Therefore blocking techniques for Real-time data should allow
to change as well. Meaning that if new records are inserted they have to be
applied to the blocked/indexed data as well.

## Dynamic Similarity-Aware Inverted Index approach

As this approach is an extension to [@CG:Scalable:08] it has the same
components. Namely a Record Index (RI) holding the reference identifiers for
each record attribute, the Block Index (BI) storing the unique attribute values
assosiated with the RI keys and a Similarity Index (SI) holding the
pre-calculated similarities between attribute values in the same block.

**Build Time**. Building the Indexes is equal to the original approach. Insert
or append to RI then insert into BI or if appending to BI calculate the
similarities insert into SI and add new similiarity from all entries of BI into
SI.

**Query Time**. Works the same as the original approach if the record attribute
can be found in the RI. Then insert RI retrived list into accumulator with
similarity 1 then insert all entries in SI with their identifiers from RI and
similarity values into the accumulator. If record attribute is not available
insert it into the indexed before executing the search. Thereby the extending
the index with the new record.

## Frequency-Filtered Index

As this index can become quite large it is wise to reduce the amount of indexed
records to the most frequent. As many real world datasets follow zips law,
meaning there are few frequent attribute and many infrequent ones, the index can
be optimized to only index most x% frequent values. This requires an list of
the most frequent attritbutes which needs to be provided. I.e. by analysing
available dictionaries.

## Evaluation

On a dataset with 2.5 million records the authors show that time needed to
insert a single records is almost constant and thereby independent of the
dataset size. Times average around 0.1 msec. The query time is also not effected
by the growing index and averages around 0.1 sec.

The result from the frequency filtering show that the amount of memory can
almost be halfed if only the top 10% frequent values are index. With 30% there
is only a 2% drop in recall.
