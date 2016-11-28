# Adaptive Duplicate Detection Using Learnable String Similarity Measures

This paper present a framework for improving duplicate detection with trainable
measures of textual simularity. Thereby it differanties between character based
and token based measure. The former through edit distance and the latter through
vector-space using TF.IDF.

Accurate simularity requires adapting the string simularity metric for each
field of a tupel according to the data domain. The get the best results a
training based system must use a two step approach. Step one is field based and
step two is record based.
