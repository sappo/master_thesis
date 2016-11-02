# Adaptive Windowing for DD

This paper introduces a alternative method of Sorted Neighborhood that resizes
its window according to the number of duplicates found.

## Problems with SNM

If the window size is too small, duplicates are missed. On the other hand if the
window size is too big unnecessary comparisions are performed. Even with the
ideal windows size which is equal to the size of the largest cluster a lot of
unnecessary comparisions are performed. This is due to dirty real world data
which results in few large and many small clusters.

## Duplicate Count Strategy

Assumption: The more duplicates are found in close proximity the larger the
window. If no duplicate found in close proximity there are none or they are very
far from each other.

Thus increase the windows size according to the average duplicates found in the
current windows. To reduce the number of comparisions calculate the transitive
closure.

## Conclusion

DCS++ is more efficient than SNM without loss of effectiveness. DCS++ uses
transitive closure thus an effective algorithm is needed.
