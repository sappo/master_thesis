---
# Expose Masterarbeit

author: Kevin Sapper
title: Analyse, Design, Entwicklung und Evaluation eines skalierbaren, Nahe-Echtzeit Entity Resolution Framework für Streaming-Daten
referent: Prof. Dr. Adrian Ulges
coreferent: Prof. Dr. Reinhold Kröger
handler: Thomas Strauß (Universum Group)
company: Detim Consulting GmbH / Universum Group

bibliography: ../thesis.bib
csl: din-1505-2-numeric.csl
link-citations: true
nocite: |
---

# Einleitung

Die Masterarbeit soll in Zusammenarbeit mit der Firma Detim Consulting GmbH
geschrieben werden. Dazu wird ein Problemfeld bei dem Kunden Universum Group in
dessen Geschäftsfeld Inkasso-, Liquiditäts-, und Risikomanagement gewählt.

# Problemfeld Universum Group

Die Universum Group bietet Lösungen für Onlineshops zur Bonitäts- und
Adressprüfung, sowie zum Forderungsankauf der Onlineshop-Kunden. Dabei wird dem
Händler bei entsprechender Bonität seines Kunden das Angebot gemacht, die
Forderung nach Ablauf einer Zahlungsperiode zu 100 % zu übernehmen. Damit eine
möglichst zuverlässige Aussage über die Bonität des Kunden getroffen werden
kann, muss zunächst herausgefunden werden, ob der Kunde bereits bei der
Universum Group bekannt ist. Das Problem an dieser Stelle ist, dass der Kunde
seine Daten Online selbst erfasst und diese nicht anhand von Personalausweis
oder ähnlichen Dokumenten überprüft werden können. Fehler bei der Datenerhebung
sind beispielsweise unterschiedliche Schreibweisen, insbesondere bei Adressen,
Tippfehler, welche bei Namen nicht offensichtlich sind, unterschiedliche
Konventionen, etwa Str. für Straße, oder akademische Titel und Adelstitel,
welche in Onlineformularen nicht standardisiert erfasst werden. Bei der
Bonitätsprüfung dient die Personenidentifizierung dazu, Kunden mit positiver
oder negativer Zahlungsmoral zu erkennen und anzunehmen bzw. abzulehnen. Je
genauer die Personenidentifikation ist, desto aussagekräftiger sind die
Bonitätsauskunfte von externen Dienstleistern, beispielsweise der Schufa. Beim
Inkassomanagement gilt zudem das sog. Schadensminderungsprinzip. Das bedeutet,
das alle angekauften Forderungen eines Kunden nur einmalig abgemahnt werden
dürfen. Daher müssen hier Personendubletten gefunden und zusammengeführt werden.

Das aktuelle System zur Personenidentifizierung funktioniert nur bei der
Bonitätsprüfung und ist durch einen externen Dienstleister realisiert. Dieser
bereinigt und prüft Namen und Adressen. Allerdings skaliert das System dabei nur
innerhalb eines vorgegebenen monatlichen Kontingents.

# Duplikatserkennung

Die Methoden zur Duplikatserkennung stammen ursprünglich aus dem
Gesundheitsbereich (Felegi & Sunter 1969). Je nach Fachgebiet gibt es
unterschiedliche Fachbegriffe. Statistiker und Epidemiologen sprechen von
*record* oder *data linkage*, während Informatiker das Problem unter *entity
resolution*, *data* oder *field matching*, *duplicate detection*, *object
identification* oder *merge/purge* kennen. Dabei geht es nicht um die reine
Personenidentifikation, sondern vielmehr um die Identifikation von Entitäten
aller Art, beispielsweise Kunden, Patienten, Produkte oder Orte. Dabei können
die Entitäten nicht durch ein einzigartiges Attribut identifiziert werden. Zudem
sind die Datensätze oft fehlerhaft, beispielsweise durch Rechtschreibfehler oder
unterschiedliche Konventionen. Die Methoden zur Entitätsauflösung arbeiten meist
auf Datensatzpaaren und liefern als Ergebnis eine Menge von Übereinstimmungen.
Eine Übereinstimmung verknüpft zwei Entitäten. Zusätzlich kann über einen
optionalen Ähnlichkeitswert (engl. similarity score), normalerweise zwischen 0
und 1, die Intensität der Übereinstimmung angegeben [@KR:Frameworks:10].

Zur Bestimmung der Ähnlichkeit eines Datensatzpaares unterscheiden Elmagarmid et
al. [@EIV:Duplicate:07] zwischen Attributsvergleichs- (engl. field
matching) und Datensatzvergleichsmethoden (engl. record matching). Methoden zum
Attributsvergleich sind zeichenbasierend (edit distance, affine gap distance,
Jaro distance metric oder Q-gram distance), tokenbasierend (atomic strings,
Q-grams mit tf.idf), phonetisch (soundex) oder nummerisch. Die
Datensatzvergleichsmethoden sind probabilistisch (Naive Bayes), überwachtes bzw.
semi-überwachtes Lernen (SVMLight, Markov Chain Monte Carlo), aktives Lernen
(ALIAS), distanzebasierend (siehe Attributsvergleich - Datensatz als
konkatenierter String) oder regelbasierend (AJAX). Die Ausführung der
Vergleichsmethoden ist enorm teuer, da diese das Kreuzprodukt zweier Mengen
bilden müssen. Um die Ausführungszeit zu reduzieren, wird versucht, den Suchraum
auf die wahrscheinlichsten Duplikatsvorkommen zu begrenzen. Diese Vorgehen
werden als Blocking oder Indexing bezeichnet. Elmagarmid et al. nennen Standard
Blocking, Sorted Neighboorhood Approach, Clustering und Canopies, sowie Set
Joins als Vorgehensweisen. (Referenzen zu den Methoden folgen noch!)

Da es keine Methode zur Entity Resolution gibt, welche allen anderen überlegen
ist, wurden Ende der 90er Jahre begonnen, Frameworks zu entwickeln, welche
verschiedene Methoden miteinander kombinieren. Einen Vergleich dieser Frameworks
wurde durch Köpcke & Rahm 2010 [@KR:Frameworks:10] durchgeführt. Ein
Framework besteht aus verschiedenen Matchern. Ein Matcher ist dabei ein
Algorithmus, welcher die Ähnlichkeit zweier Datensätze ermittelt. Ähnlich wie
Elmagarmid et al. unterscheiden Köpcke & Rahm zwischen attributs- und
kontextbasierenden Matchern. Als Kontext bezeichnen Sie die semantische
Beziehung bzw. Hierarchie zwischen den Attributen. Um die Matcher miteinander zu
kombinieren nutzen die Frameworks min. eine Matching Strategie. Eine Strategie
ist, die Ähnlichkeitswerte verschiedener Matcher nummerisch zu kombinieren,
beispielsweise durch eine gewichtete Summe oder einen gewichteten Durchschnitt.
Ein anderer Ansatz ist regelbasierend. Eine einfache Regel besteht aus einer
logischen Verbindung und einer Match-Kondition, beispielsweise einem
Schwellenwert. Die dritte und komplexeste Strategie ist Workflow-basierend.
Hierbei kann beispielsweise eine Sequenz von Matchern die Ergebnisse iterativ
einschränken. Grundsätzlich können Workflows beliebig komplex werden. Einen
passenden Workflow zu finden, kann selbst Domainexperten vor eine große
Herausforderung stellen. Daher gibt es trainingbasierende Ansätze, passende
Parameter für Matcher oder Kombinationsfunktionen (z.B. Gewicht für Matcher) zu
bestimmen. Solche Ansätze sind etwa Naive Bayes, Logistic Regression, Support
Vector Maschine oder Decision Trees. (Referenzen zu den Ansätzen folgen noch!)

Ein Großteil der Forschung in Entity Resolution konzentriert sich auf die
Qualität der Vergleichsergebnisse. Die von Köpcke & Rahm verglichenen Frameworks
konzentrieren sich allesamt darauf, zwei statische Mengen miteinander zu
vergleichen. Bei großen Datenmengen kann dies durchaus mehrere Stunden dauern.
Daher gibt es in den letzten Jahren einige Ansätze und Frameworks, welche
MapReduce zum Skalieren nutzen [@KR:Parallel:13;@MAS:Graph:14]. Zudem gibt es
immer mehr Bedarf, Vergleichsergebnisse in Nahe-Echtzeit zu liefern. Erste
Ergebnisse, Entity Resolution skalierbar und in Nahe-Echtzeit zu erreichen,
präsentieren Christen & Gayler in [@CG:Scalable:08] 2008 unter Verwendung
von Inverted Indexing Techniken, welche normalerweise bei der Websuche Anwendung
finden. Dabei betrachten Sie vor allem die Anforderungen eines Anfragestroms
(engl. query stream). Ihre Anforderungen sind, einen Strom von Anfragedatesätzen
gegen potentiell riesige Datenmengen im Subsekundenbereich pro Anfrage
abzuarbeiten. Dabei sollen die Treffer der Anfrage mit einem Ähnlichkeitswert
versehen sein. Zudem muss es möglich sein, die Menge an Anfragen zu skalieren.
Das Hauptproblem ist hierbei die Skalierung. Um skalieren zu können, wird
versucht, die Abarbeitung des Suchraums zu parallelisieren. Eine Studie von
Kwon, Balazinska, Howe, & Rolia [@KBHR:study:11] in MapReduce Anwendungen
zeigt, das selbst geringe Ungleichgewichte bei der Verteilung des Suchraum auf
Mapper bzw. Reducer, aufgrund der Komplexität der Matching Algorithmen zu
deutlich längeren Laufzeiten und damit Gesamtlaufzeiten führt. In einem ihrer
Beispiele sind bei einer Gesamtzeit von 5 Minuten die meisten Mapper innerhalb
von 30 Sekunden fertig. Auch beim Streaming kann diese sog. Datenschiefe (engl.
data skew) den Durchsatz eines Clusters signifikant mindern. Einen weiteren
Ansatz, die Laufzeit für Nahe-Echtzeit Anwendungen zu optimieren, präsentieren
Whang et al. [@WMG:Pay:13]. Anstatt eine Ergebnismenge nach
Abschluss eines Algorithmus zu liefern, zeigen Sie Möglichkeiten, partielle
Ergebnisse während der Laufzeit des Algorithmus zu erhalten.

# Zielsetzung {#sec:ziele}

Im Rahmen der Thesis soll ein Entity Resolution Framework für Datensatzströme
entstehen. Als Basis soll ein Stream Processing Framework, beispielsweise aus
der Apache Familie (Flink, Samza, Spark, Storm, etc.) oder ein (Complex) Event
Processing Framework, beispielsweise Esper, genutzt werden. Das Framework soll
eine Reihe von Matchern sowie Kombinationsfunktionen der Matcher unterstützen.
Die Implementierung der Matcher soll größtenteils aus Standard-Bibliotheken
erfolgen. Auch bei den Maschine Learning Kombinationsfunktionen soll
weitestgehend existierende Lösungen, etwa WEKA [@HFH.EA:WEKA:09], dass auch im
dedoop Framework [@KR:Parallel:13] Anwendung findet, genutzt werden. Das
Hauptaugenmerk der Thesis hingegen soll die Skalierbarkeit sein. Dabei muss ein
existierender Datenbestand zunächst so geclustert werden, dass die Entity
Resolution in jedem Cluster möglichst gleich lange dauert. Bei MapReduce
Anwendungen kann auf Basis der bekannten Datenmengen die Verteilung der
Entitäten, sowie die Größe und Anzahl der Cluster berechnet werden. Dadurch wird
das Data Skew Problem minimiert, sodass alle Mapper bzw. Reducer eines
MapReduce-Jobs eine ähnliche Laufzeit haben. Beim Streaming hingegen kommen neue
unbekannte Datensätze in das System. Ein Cluster kann daher zunächst nur auf
Basis der existierenden Datensätze gebildet werden und ist abhängig von der
gewählten Blocking Strategie. Damit die Latenzen möglichst gering bleiben,
sollten die einzelnen Cluster eine bestimmte Größe nicht überschreiten. Um den
Durchsatz innerhalb des Systems zu optimieren muss ein Load-Balancing
durchgeführt werden. Dadurch soll verhindert werden das Backpressure auftritt
und schlimmstenfalls Datensätze verloren gehen. Eine weitere Schwierigkeit ist,
dass die Datenmenge nicht statisch ist, sondern neue Datensätze jederzeit
hinzukommen können. Dabei muss betrachtet werden, ob die Blocking Strategie bzw.
das Framework es zulässt das Cluster während der Laufzeit zu verändern. Zudem
kann das Clustering bzw. das Load-Balancing auch statistische Daten heranziehen,
beispielsweise das bei einer weltweiten Personenidentifikation tageszeitabhängig
mehr Anfragen aus Europa, Asien oder Amerika kommen. Des Weiteren muss das
Framework mindestens zwei Blocking Strategien implementieren, damit möglichst
viele Duplikate gefunden werden können.

Während der Analyse sollen typische Streamingszenarien betrachtet, etwa ein
kontinuierlicher Datenstrom kleiner Datensätze mit zwischenzeitlichen Peaks
unterschiedlicher Länge. Unbekannte Entitäten, d. h. Entitäten für welche die
Ergebnismenge der Entity Resolution leer ist, sollen als neue Entitäten in den
Datenbestand aufgenommen werden. Ein interessantes Szenario diesbezüglich kann
sein, kleiner Datenbestand mit vielen neuen Entitäten, da hier das System
potentiell die schwierigste Phase durchlaufen muss.

Idealerweise soll der Durchsatz sowie die Qualität der Suchergebnisse mit
bereits bekannten Veröffentlichungen verglichen werden. Da diese meist auf
statischen Daten arbeiten, müssen die zu prüfenden Datenmenge(n), für einen
Vergleich, künstlich in das System gestreamt werden.

# Methoden

Zur Umsetzung der in [@sec:ziele] beschriebenen Ziele muss zunächst eine
Wissensbasis durch Literaturarbeit in folgenden Grundlagen geschaffen werden:

* Algorithmen zur Entity Resolution
* Blocking und Indexing Strategien für Entity Resolution
* Data Skew bei verteilten und parallelen Anwendungen
* Load-Balancing für Streaminganwendungen
* Entity Resolution Frameworks - traditionell, MapReduce, Streaming
* Streaming Processing Frameworks/(Complex) Event Processing Frameworks

Weitere Methoden sind:

* UML-Entwurf
* Proof of Concept
* Funktionelle Leistungsbewertung anhand von Datensätzen in wissenschaftlichen
  Publikationen

# Erwartete Ergebnisse

Die erwarteten Ergebnisse der Masterarbeit sind:

* Analyse von Entity Resolution Algorithmen
* Analyse von Entity Resolution Frameworks
* Analyse von Stream Processing Frameworks und ggf. (Complex) Event Processing
  Frameworks
* Analyse der Data Skew und Load-Balancing Problematik für Entity Resolution
* Design eines Entity Resolution Streaming Framework
* Prototyp der wesentlichen Funktionen
* Evaluation des Prototypen gegen öffentliche Datensätze existierender
  Veröffentlichungen

# Vorbedingungen

* Datensätze zum Evaluieren und Trainieren des Frameworks bzw. der Algorithmen
  [@HCTL:Duplicate:03;@KTR:Evaluation:10;@DN:DuDe:10]

# Literatur
