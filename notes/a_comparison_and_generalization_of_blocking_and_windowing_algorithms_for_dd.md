# A comparison and generalization of blocking and windowing algorithms for DD

This paper performs a evaluation between Standard Blocking and Sorted
Neighborhood. From the results it introduces the Sorted Blocks
blocking/windowing method for ER.

## Standard Blocking

Partitions sets of tuples into disjoint partitions (blocks). All tuples within
each block are compared. Blocking result depends on a good partition predicate
which controls number and size of the blocks. To detect duplicates in different
partitions multi-pass blocking is applied.

## Sorted Neighborhood

Step one assign sorting key to each tuple (must not be unique). Step two sort
tuples according to thier sorting key. Final step slide a windows of fixed size
across the sorted tuples and compare all tuples within the window. To avoid
miss-sorts used multi-pass variants with differnt sorting keys per tupel.

## Comparision

* Both rely on oderings
* Both assume that tuples close to each other hava a higher chance of being
  duplicates.
* Both methods perform approximatly the same total number of comparisions.
  Though the actual comparisions differ.
* SB applies no overlap of partitions
* SN applies total overlap of partitions

## Sorted Blocks

Sorted Blocks aim to optimize the overlap between partitions. As SB and SN are
the two extrem examples this algorithm is a combination of both. Assumption is
that the realy overlap should be big enough that real duplicates are detected
but not too high in order to reduce the number of comparisions.

Idea: First sort all tuples, then partition recored into disjoint sorted subsets
and finally overlap partitions. The number of comparisions can be controlled the
size of the overlap $u$ e.g. $u=3$.

Within each block every tuples is compared with each other. Within the overlap
window $u+1$ which is slid across the partitions the first tuple of the windows
is compared with the remaining.

The overall complexity is $O(n(\dfrac{m}{2}+\log n)).
