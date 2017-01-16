# An Unsupervised Algorithm for Learning Blocking Schemes

This paper introduces algorithms to easily generate blocking keys for dataset
without properly labeled data.

When generating blocking keys usually a domain expert is required to formalize a
proper key. But even for such an expert is very difficult to choose a good one.
Another method is to learn the blocking key given enough properly labeled data
which is not the case for most datasets. Thus as a first step a algorithm to
generate a weak label set if performed. With those the actual blocking key can
be learned.

## Blocking Scheme Definition

* indexing function $h_i : Dom(h_i) -> U*$ takes the field value $x_t$ of a
  tupel t as input and return all set of zero or more Blocking Key Values
  (BKVs).

* general blocking predicate $p_i : Dom(h_i) x Dom(h_i) -> {True, False}$ takes
  input field $x_{t1}$ and $x_{t2}$ from two tupels t1 and t2 and return True if
  both of common BKVs otherwise False.

* specific blocking predicate $(p_i, f)$ is a pair where $p_i$ is a general
  blocking predicate and f is a field. As specific blocking predicate takes two
  tupels $t1$ and $t2$ as input and applies $p_i$ to the according fields $f1$
  and $f2$.

* DNF blocking scheme $f_P$ is a function constructed in Disjunctive Normal Form
  using a given set $P$ of specific blocking predicates or terms which are
  conjunctions of specific blocking predicates.

## Blocking step

Applying the DNF blocking schme $f_P$ on a relation $R$ is achieved by appling
the indexing functions of each term to each tupel $t$ in $R$. For a term $C$ of
specific blocking predicates a cross product of the indiviual result sets is
generated as BKVs. Each BKV forms a block and a tupel is assigned to each
BKV-Block.

## Generating Weakly Labeled Training Set

