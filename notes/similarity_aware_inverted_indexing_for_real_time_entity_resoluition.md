# Similarity Aware Inverted Indexing for Real-time Entity Resolution

Collection of 3 papers which discuss similarity aware inverted indexing for
real-time entity resolution and build upon each other:

* Towards Scalable Real-Time Entity Resolution using a Similarity-Aware
  Inverted Index Approach (2008)
* Dynamic similarity-aware inverted indexing for real-time entity resolution
  (2013)
* A Two Stage Similarity-aware Indexing for Real-time Large Scale Entity
  Resolution (2013)

## Towards Scalable Real-time Entity Resolution Using a Similarity-aware Inverted Index Approach

This paper dicusses the challanges for Entity Resolution in Real-time system,
i.e. data or event streaming. Therefore the authors propose an Inverted Index
algorithm with three variations which improve matching speed but a the cost of
matching quality.

### Requirements Real-time ER

The requirements for a Real-time ER framework is to process a stream of query
records as fast as possible against a (large) data set of existing entities. The
response time for such a system must be short (ideally sub-second). The result
of a query is a ranked list with probabilities that a matched record refers to
the same entity.

### Default  Inverted Index ER

Phase 1: Using a static database, which is assumed to be clean (=deduplicated),
an Inverted Index is build using a record attribute or attribute encodings i.e.
Soundex.

Phase 2: Build index is queried by a stream of records. For each record a list
of top randked records is obtained from the index.

### Similarity-Aware Inverted Index

Main idea is to pre-calculate similarities between attributes in the same block.

**Build-time.** Uses three Indexes using actual record values rather then
encodings. For each unique attribute being used a blocking key a Record Index
(RI) is build which stores all unique attributes and their associated record
identifiers. Then the Block Index (BI) with an encoding of the attribute(s) is
build. Which stores a list of blocking key values used in RI. Lastly the
Similarity Index (SI) is build which has the same key as (RI) and holds the
similarity values of each record in the same block. Inserting new records is
quite efficient because only similarity values according the to new record have
to be calculated.

**Query-time**. In the *first* case a query record attribute is available as
blocking key in RI. All records in this index are inserted into the
*accumulator* with similarity 1.0. All other records from the same block are
retrieved from SI correlated to RI and inserted with their similarity. In the
second case when a query record attribute is not available as blocking key the
encoding is calculated. Then for each record in the block the similarity is
calculated and records and similarity values are added into the *accumulator*.
The accumulator contains a list of possible matches which can be sorted by their
similarity score.

#### Materialized Similarity-Aware Inverted Index

This is an optimization which aims to improve retrival time at the cost of
memory usage. Therefore the similarity values are stored in the Record Index
(RI). Further the Record Index now contains all records within the same block
with their according similarities. During query time the a record attribute
found in the Record Index simply return its list which equals the accumulator.

#### Further Optimization

Only insert values into the accumulator that hold to a certain threshold.

### Summary

While the Inverted Index approach significantly outperforms Standard Blocking
and achieves good results for records with minor, i.e. only one mistake, it
fails short of finding duplicates with many (3+) mistakes. Also the required
amount of memory for the materialized approach is at least 15 times higher than
Standard Blocking.

## Dynamic similarity-aware inverted indexing for real-time entity resolution

This paper improves the Similarity-Aware Inverted Index approach from
[@CG:Scalable:08] to allows dynamic additions to the index. Also it investigates
the frequency-distribution of data and the effect of reducing the index to hold
only frequent records.

In recent years dynamic entity resolution becomes more and more important as
many businesses used databases that are not static and change over time.
Therefore blocking techniques for Real-time data should allow to change as well.
Meaning that if new records are inserted they have to be applied to the
blocked/indexed data as well.

### Dynamic Similarity-Aware Inverted Index approach

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

### Frequency-Filtered Index

As this index can become quite large it is wise to reduce the amount of indexed
records to the most frequent. As many real world datasets follow zips law,
meaning there are few frequent attribute and many infrequent ones, the index can
be optimized to only index most x% frequent values. This requires an list of
the most frequent attritbutes which needs to be provided. I.e. by analysing
available dictionaries.

### Evaluation

On a dataset with 2.5 million records the authors show that time needed to
insert a single records is almost constant and thereby independent of the
dataset size. Times average around 0.1 msec. The query time is also not effected
by the growing index and averages around 0.1 sec.

The result from the frequency filtering show that the amount of memory can
almost be halfed if only the top 10% frequent values are index. With 30% there
is only a 2% drop in recall.

## A Two Stage Similarity-aware Indexing for Real-time Large Scale Entity Resolution

This paper improves the Similarity-Aware Inverted Index approach from
[@CG:Scalable:08] with Local Sensitive Hashing (LSH). It also uses the idea
introduced by [@RCL+:Dynamic:13] to dynamically extend the inverted index during
query time.

### Local Sensitive Hashing (LSH) with Minhash

The idea of LSH is that neighborhood items in a high dimensional space are very
likely to stay close after being projected on a lower dimensional space. Minhash
is an efficient estimation of two set known as Jaccard similarity. Through LSH
it is possible to reduce the search space by grouping similar items. Therefore
for each item mulitple hashes are created. Each hash is a signature for the item
and all hashes together form a signature matrix. One way to group similar items
is to put items with the same hash value into the same bucket. The hope is that
dissimilar items are not hashed into the same bucket. To avoid dissimilar items
being put into the same bucket a signature matrix is divided in $b$ bands with
$r$ rows. For example a signature matrix with 12 rows and 3 row per band is
divided into 4 bands. While it is likely that dissimlilar items have common
hashes it is very unlikely that they have common bands.

### Two Stage Approach

**Build Time**. For each MinHash band of each record a bucket is created and the
record is put into the buckets. The bucket collection is called LSH Index (LI).
Thereby the LI replaces the RI index in DySimII. Building the Block Index (BI)
and Similarity Index (SI) is similar to the dynamic approach.

**Query Time**. The first step is to obtain all records which are hashed into
the same buckets from LI. Then for each record obtained the attributes are
compared with the values stored in the similarity index (SI).

### Summary

The results show that a query is about 10 times faster then DySimII without
obvious memory increase. However building the index takes about 3 times longer.
Also the loss in recall is only marginal.
