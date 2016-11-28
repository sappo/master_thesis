# Context-Aware Approximate String Matching for Large-Scale Real-Time Entity Resolution

This paper introduces a string matching algorthim for real-time entity
resolution that incorperates contextual information into simularity calculation.
These context information are frequencies of two strings to be matched,
likelihood of edits between them and number of other strings that are highly
similar. As this paper addresses real-time entity resolution the data are
pre-calculated with an Index.

## Building the Index

For each attribute a and EDIndex is generated. The EDIndex consists of an
interted index of all strings in attribute a with their frequencies and record
identifiers. A graph of string pairs within a maximum edit distance of m and and
inverted index of edit path and their frequencies.

Re-implement to understand the rest of the paper

## Summary

Taking edit frequency and string neighborhood into consideration can lead to
improvements in matching quality. However both string frequency and string
inverse document frequency make things worse.

This approach can be integrated with Towards Scalable Real-Time Entity
Resolution using a S imilarity-Aware Inverted Index Approach for example.
