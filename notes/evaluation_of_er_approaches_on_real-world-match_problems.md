# Overview

This paper evaluates non-learning and learning approaches against real-world
matching Problems. Namely DBLP-ACM, DBLP-Scholar, Amazon-GoogleProducts and
Abt-Buy (<source>-<target>). It differentiates between 1 or 2 attributes for
matching. The Blocking stratagie is the same for all approaches. The evaluation
considers both quality in F-Measure and execution time in seconds. Compared
framworks are FEBRL, MARLIN, FEVER and a non disclosed comercial one.

The approaches differ only in the parameters *function* which determines the
similarity between to data sets and *threshold* which identifies a match or
non-match. The ML approaches are feed with the same training data which is
provided in pairs 20, 50, 100 and 500. To ensure a decent quality of training
data a ratio is applied that ensure a minimum of 40% of matches or non-matches.

# Evaluation

**Non-Learning based approaches** show a high effectivness for the bibliographic
match task with F-Measure results above 91% for most functions. The e-commerce
match task turned out to be much more challanging with F-Measure result only at
62% for (Amazon-GoogleProducts) and 70% for (Abt-Buy). Interessting is that
taking a second attribute into consideration turned out to reduce the overall
qualtity of the matching result. Regarding execution times FERBL turned out to
be much slower than the others. Using a second attribute slowed down the
execution time by a factor of 2.

**Learning based approaches** achive stable result for easy bibliographic
matching with a small training size of 20. More challanging biblographic
matching works best with SVM stratagies and combining several matchers reaching
an F-Measure about 88-89%. All stratagies have simialar difficulties as
non-learnears with e-commerce data. With smaller training sizes than 500 the
results are substantially bad. In general performs a 2-Step learning better than
1-Step learning. Regarding the execution times the learning based approaches are
significantly worse than the non-learning ones. Even worse is that combined
approaches comparing two attributes are at least factor 2 slower than other
learning-based approaches. Though the combined approach for learning-based
approaches always improves the matching result.

# Outlook

The good quality of learning based approaches with two attributes comes at
expense of significantly higher execution times. Thus it is doubtful if these
approaches do scale. Non-learning based single attribute matching outperform
learning-based matching in both quality and exection time.
