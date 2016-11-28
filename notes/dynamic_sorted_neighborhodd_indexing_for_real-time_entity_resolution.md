#  Dynamic Sorted Neighborhood Indexing for Real-Time Entity Resolution

This paper proposes a Sorted Neighborhood Indexing approach for Real-Time Entity
resolution. Therefore instead of using a static array as datastructure the
propose a tree-based technique and introduce many popular variations of the
classic SNM with adaptive windowing. Also they enhance query time by
pre-calculating attribute scores.

The proposed approach underlies the assumption that every query record is added
to the index. By doing so the history of queries and changes in a address for
example wont get lost which might be useful for a credit bureau.

**Challenge** in Real-Time Indexing is to develop indexding techniques that
allow dynamic updates and facilitye ral-time matching by generating a small
number of high-quality candidate records that are to be compared.

**Problem** for Real-Time ER: for each query record $q_j$ in a query stream $Q$,
find all the records in $R$ that belong to the same entity as $q_j$, denoted as
the set $M_q$, in subsecond time, $M_{q_j} = \{r_i|r_i.eid = q_j.eid, r_i \in
R\}, M_{q_j} \subseteq R, q_j \in Q$.

## Data Structure

BraidedTree (BRT) is a balanced binary AVL tree where each node in the tree has
a link to its predecessor and succesor nodes according to an alphabetical
sorting of the key values in the nodes. A node consists of it's sorting key
(SKV), a list of nodes with this sorting key and a link its predecessor and
succesor. A query node (i.e. the node where a query record has been sorted in)
is denoted as $N_q$.

## Dynamic Sorted Neighborhood Indexing (DySNI)

The first assumption is that all records are kept unmodified after creation
since the can provide evidence about earlier requests. DySNI has a inital build
phase and a query phase similar to DySimII.

**Build Phase**. The loads records from a possible empty dataset $R$ into the
BRT. In a first step the SKV for a record $r$ is generated. Which may be a
single attribute or a concatenation of multiple. If the SKV is new a new node is
created in the tree. If the SKV already exists the query record is added to an
existing node. The complete list of records $R$ are also indexed into an
inverted list $D$ so they can be retrieved for a fast attribute by attribute
comparision.

**Query Phase**. As said earlier the assumption is that all records are inserted
into the index. Therefore a SKV is generated for a query record $q$ together
with a new unique record identifier $q.id$. The SKV and $q.id$ is then inserted
into the BRT as decribed in the build phase. The query record is added to $D$ as
well.

Now the window of neighboring nodes can be generated. All records identifiers
that are stored in the window's nodes are added the a candidate record set $C$.
The whole records from $D$ are then retrieved for all records in $C$ and a pair
comparision for all records is performed. The compared candidate records are
return in the list $M$ which is sorted by the overall similarity. For generating
the window neighbors this paper introduces 4 approaches.

### Fixed Window Size (DySNI-f)

This approach in based on the classical SNM from Hernández & Stolfo. The window
is set as number of neighboring tree nodes in one direction (previous or next).
The window is set as number of neighboring tree nodes in one direction (previous
or next) of the query Node $N_q$. A window of size $w=0$ refers to the query
node $N_q$ only. A fixed-size window can lead to both unnecessary comparision
with records in nodes that are unlikely to have a high enough similarity, as
well as potential true matches outside the window.

### Candidates-Based Adaptive Window (DySNI-c)

This apprach aims at matiching a certain minimum number of records. The total
minimum number to records to be return as candidates is denoted as $\delta$. The
initial candidate set contains only the records in the query node $N_q$. The
decision to expand on both sides is made if the count of records at the qurey
record's $N_q$ is smaller than the minimum threshold $|C| < \delta$. The
remaining total records to reach is calculated by $r = \delta - |C|$. The
expansion threshold for each direction is then set to $\lceil r/2 \rceil$.

### Similarity-Based Adaptive Window (DySNI-s)

This is based on the approach from Yan et al. which uses similarities between
SKVs to expand or shrink the window size and move over a static array from first
to last entry. The approach for the BRT is to seperatly expand the window into
either direction. The window is initialized with $w=0$. The Window is expanded
into one direction and the similarity between query node's SKV and SKV of prev
or next SKV is calculated. If the similarity is above a certain threshold
$\Delta$ the window is expanded. This is repeated as long as the next SKV in
that direction is above the threshold.

### Duplicate-Based Adaptive Window (DySNI-d)

The original appraoch by Draisbach et al. grows or shrinks the windows size
based on the number of classified matches found. The approach for the BRT is to
seperatly expand the window on each side of the node. The window has an initial
size of $w>=1$. For each side (prev and next) a candidate list is calculated
independently. Then without adding records from $N_q$ the matches to $q$ are
calculated. If the amount of matches found are above a threshold $\delta$ the
window is expanded, otherwise abort.

## Similarity-based Dynamic Sorted Neighborhood Indexing (SimDySNI)

The SimDySNI approach add to list to a node inside the BRT, namely, $S_p$ and
$S_n$ which contain the precalculated similarities between this node's SKV and
the SKV of all neighboring nodes. The build phase is the same as for DySNI.
However afterwards the similarities between nodes have to be calculated. This is
done according to the choosen method for generating the window. For DySNI-f the
similarities within a window of $w$ are precalculated. For the adaptive window
the similarites are calculated accoring the the threshold choosen. During query
time a new nodes similarites have the be calculated before the actual quering
can begin.

## Multitree Dynamic Sorted Neighborhood Indexing (M-DySNI)

As the SNM method is sensitive to errors at the start of the SKV the authors
propose a multitree index. The index hereby consists of multiple tree structures
where each tree is build using a different SK. During build phase for each
record multiple SKV are generated and inserted into one tree each. At query time
a query record is inserted into all trees accordings to its SKVs. The retrivied
candidate set from each tree are united into the acutal candicate record set
$C$. The pair comparisions from hereon is the same as in DySNI.

## Analysis.

* Tree Structures (Why BRT?!)
* Estimation of the Number of Records
* Effect of using different SKs on Index Size
* Scalability Experiments (AVG insert/query time)
* Effect on using different threshold on quality and efficiency (Recall/Time)
* Effect of Having different number of duplicates (at least 5/10/20)
* Effect of Precalculating Similarities on Comparison Time
* Required Memory Size
* Effect of using multiple trees and different SK combinations (Recall/Time)
* Scalability of multiple tree index (AVG insert/query time, memory)

## Conclusion

DySNI-d approach does not work efficiently because in DySNI all records with the
same SKV are inserted into the same tree node, which limits the expansion and
reduces the quality of achived results.

DySNI-s approach showed the best recall result since the expansion depends on
similarities on SKVs which the tree is sorted by. Better recall value can be
achieved by cost of increased query time. On the other hand DySNI-f and DySNI-c
can be used when the application need to controll the time needed for resoling
queries.

SimDySNI reduces the average comparision time by 20% to 70% while it increase
the footprint by between 20% and 70%. The multitree indexing approach improved
matching quality while maintaining efficiency.

Overall the result show that SKs based on concatenation of more then one
attribute are more suitable for ER as the reduce the query time significantly
also SKs with no dependency seem to produce better result (i.e. firstname and
postcode instead of firstname and lastname).



