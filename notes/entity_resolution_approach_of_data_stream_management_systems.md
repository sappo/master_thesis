# Entity Resolution Approach of Data Stream Management Systems

This paper introduces real-time entity stream data processing architechture that
performs entity resolution on heterogenous data.

The four components need by a DSMS to process heterogenous streaming data are:

* Scalablility
* Low latency
* Common protocol
* Standardized format

## Architecture

The architecture consists of 5 main components.

**Stream receiver**. Receives input stream from various channels. For example
HTTP or ODBC. The received data is transfered to the stream filter.

**Stream filter**. Uses a query language, for example CQL or Sparql, to perform
a filtering on the incomming data stream. The filtering is done through
pattern-based queries. In order to process events and filter them those need to
be registered in the system.

**Adapter**. Which can read heterogenous stream data with various formats, i.e.
XML, JSON, CSV, ... . The read data is then transformed into standardized
format. This step is comaparable to the pre-processing in standard entity
resolution.

**Stream Entity Resolution Engine**. Resolves ambigous entity in real-time
against an existing database. Therefore a blocking index is create on the
existing data where the blocking key has to be choosen by a domain expert. The
comparator performs pairwise comparisons within the choosen block. The match or
non-match decision is made through a threshold approach.


## Conclusion

The system uses the most simplistic ER mechanism a person can think of. For this
system to be usable a lot more research has to be put in.
