# Towards Scalable Real-time Entity Resolution Using a Similarity-aware Inverted Index Approach

This paper dicusses the challanges for Entity Resolution in Real-time system,
i.e. data or event streaming. Therefore the authors propose an Inverted Index
algorithm with three variations which improve matching speed but a the cost of
matching quality.

## Requirements Real-time ER

The requirements for a Real-time ER framework is to process a stream of query
records a fast a possible against a (large) data set of existing entities. The
response time for such a system must be short (ideally sub-second). The result
of a query is a ranked list with probabilities that a matched record refers to
the same entity.

## Default  Inverted Index ER

Phase 1: Using a static database, which is assumed to be clean (=deduplicated),
an Inverted Index is build using a record attribute or attribute encodings i.e.
Soundex.

Phase 2: Build index is queried by a stream of records. For each record a list
of top randked records is obtained from the index.

## Similarity-Aware Inverted Index

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

### Materialized Similarity-Aware Inverted Index

This is an optimization which aims to improve retrival time at the cost of
memory usage. Therefore the similarity values are stored in the Record Index
(RI). Further the Record Index now contains all records within the same block
with their according similarities. During query time the a record attribute
found in the Record Index simply return its list which equals the accumulator.

### Further Optimization

Only insert values into the accumulator that hold to a certain threshold.

## Summary

While the Inverted Index approach significantly outperforms Standard Blocking
and achieves good results for records with minor, i.e. only one mistake, it
fails short of finding duplicates with many (3+) mistakes. Also the required
amount of memory for the materialized approach is at least 15 times higher than
Standard Blocking.
