---
# Expose Masterarbeit

author: Kevin Sapper
title: Analyse, Design, Entwicklung und Evaluation eines skalierbaren, Echtzeit Entity Resolution Streaming Framework
referent: Prof. Dr. Reinhold Kröger
coreferent: Prof. Dr. Adrian Ulges
handler: Thomas Strauß (Universum Group)
company: Detim Consulting GmbH / Universum Group

bibliography: ../thesis.bib
csl: din-1505-2-numeric.csl
nocite: |

---

# Einleitung

Die Masterarbeit soll in Zusammenarbeit mit der Firma Detim Consulting GmbH
geschrieben werden. Dazu wird ein Problemfeld bei dem Kunden Universum Group,
der Detim Consulting GmbH, in deren Geschäftsfeld dem Inkasso-, Liquiditäts-,
und Risikomanagement, gewählt.

# Problemfeld Universum Group

Die Universum Group bietet Lösungen für Onlineshops zur Bonitäts- und
Adressprüfung, sowie dem Forderungsankauf, der Onlineshop-Kunden. Dabei wird dem
Händler bei entsprechender Bonität seines Kunden das Angebot gemacht, die
Forderung, nach Ablauf einer Zahlungsperiode, zu 100 % zu übernehmen. Damit eine
möglichst zuverlässige Aussage, über die Bonität des Kunden, getroffen werden
kann, muss zunächst herausgefunden werden, ob der Kunde bereits bei der
Universum Group bekannt ist. Das Problem an dieser Stelle ist, dass der Kunde
Online seine Daten selbst erfasst und diese nicht anhand von Personalausweis
oder ähnlichen Dokumenten überprüft werden können. Fehler bei der Datenerhebung
sind, beispielsweise unterschiedliche Schreibweisen, insbesondere bei Adressen,
Tippfehler, welche bei Namen nicht offensichtlich sind, unterschiedliche
Konventionen, etwa Str. für Straße, oder akademische Titel und Adelstitel,
welche in Onlineformularen nicht standardisiert erfasst werden. Bei der
Bonitätsprüfung dient die Personenidentifizierung dazu, Kunden mit positiver
oder negativer Zahlungsmoral zu erkennen und anzunehmen bzw. abzulehnen. Je
genauer die Personenidentifikation ist, desto aussagekräftiger sind die
Bonitätsauskunfte von externen Dienstleister, beispielsweise der Schufa. Beim
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
*record* oder *data linkage* während Informatiker das Problem unter *entity
resolution*, *data* oder *field matching*, *duplicate detection*, *object
identification* oder *merge/purge* kennen. Dabei geht es nicht um die reine
Personenidentifikation, sondern vielmehr um die Identifikation von Entitäten
aller Art, beispielsweise Kunden, Patienten, Produkte oder Orte. Dabei können
die Entitäten nicht durch ein einzigartiges Attribut identifiziert werden.
Zudem sind die Datensätze oft fehlerhaft, beispielsweise durch
Rechtschreibfehler oder unterschiedliche Konventionen. Die Methoden zur
Entitätsauflösung arbeiten meist auf Datensatzpaaren und liefern als Ergebnis
eine Menge von Übereinstimmungen. Eine Übereinstimmung verknüpft zwei Entitäten.
Zusätzlich kann über einen optionalen Ähnlichkeitswert (engl. similarity score)
, normalerweise zwischen 0 und 1, die Intensität der Übereinstimmung angegeben
[@kopcke_frameworks_2010].

Zur Bestimmung der Ähnlichkeit eines Datensatzpaares unterscheiden Elmagarmid et
al. [@elmagarmid_duplicate_2007] zwischen Attributsvergleichs- (engl. field
matching) und Datensatzvergleichsmethoden (engl. record matching). Methoden zum
Attributsvergleich sind zeichenbasierend (edit distance, affine gap distance,
Jaro distance metric oder Q-gram distance), tokenbasierend (atomic strings,
Q-grams mit tf.idf), phonetisch (soundex) oder nummerisch. Die
Datensatzvergleichsmethoden sind probabilistisch (Naive Bayes), überwachtes bzw.
semi-überwachtes Lernen (SVMLight, Markov Chain Monte Carlo), aktives Lernen
(ALIAS), distanzebasierend (siehe Attributsvergleich - Datensatz als
konkatenierter String) oder regelbasierend (AJAX). Die Ausführung der
Vergleichsmethoden ist enorm teuer, da diese das Kreuzprodukt zweier Mengen
bilden müssen. Um die Ausführungszeit zu reduzieren wird versucht den Suchraum
auf die wahrscheinlichsten Duplikatsvorkommen zu begrenzen. Diese Vorgehen
werden als Blocking bezeichnet. Elmagarmid et al. nennen Standard Blocking,
Sorted Neighboorhodd Approach, Clustering und Canopies, sowie Set Joins als
Vorgehensweisen. (Referenzen zu den Methoden folgen noch!)

Da es keine Methode zur Entity Resolution gibt, welche allen anderen überlegen
ist, wurden Ende der 90er Jahre begonnen Frameworks zu entwickeln, welche
verschiedene Methoden miteinander kombinieren. Einen Vergleich dieser Frameworks
wurde durch Köpcke & Rahm 2010 [@kopcke_frameworks_2010] durchgeführt. Ein
Framework besteht aus verschiedenen Matchern. Ein Matcher ist dabei ein
Algorithmus, welcher die Ähnlichkeit zweier Datensätze ermittelt. Ähnlich wie
Elmagarmid et al. unterscheiden Köpcke & Rahm zwischen Attributs- und
Kontextbasierenden Matchern. Als Kontext bezeichnen Sie die semantische
Beziehung bzw. Hierarchie zwischen den Attributen. Um die Matcher miteinander zu
kombinieren nutzen die Frameworks min. eine Matching Strategie. Eine Strategie
ist, die Ähnlichkeitswerte verschiedener Matcher nummerisch zu kombinieren,
beispielsweise durch eine gewichtete Summe oder einen gewichteten Durchschnitt.
Ein anderer Ansatz ist Regel-basierend. Eine einfache Regel besteht aus einer
logischen Verbindung und Match-Konditionen, beispielsweise einem Schwellenwert.
Die dritter und komplexeste Strategie ist Workflow-basierend. Hierbei kann eine
Sequenz von Matchern die Ergebnisse iterativ einschränken. Einen passenden
Workflow zu finden kann selbst Domainexperten vor eine große Herausforderung
stellen. Daher gibt es trainingbasierende Ansätze passende Parameter für Matcher
oder Kombinationsfunktionen (z.B. Gewicht für Matcher) zu bestimmen. Solche
Ansätze sind etwa, Naive Bayes, Logistic Regression, Support Vector Maschine
oder Decision Trees. (Referenzen zu den Ansätzen folgen noch!)

Ein Großteil der Forschung in Entity Resolution konzentriert sich auf die
Qualität der Vergleichsergebnisse. Die von Köpcke & Rahm verglichenen Frameworks
konzentrieren sich alle Samt darauf zwei statische Mengen zu miteinander
vergleichen. Bei großen Datenmengen kann dies durchaus mehrere Stunden dauern.
Daher gibt es in den letzten Jahre einige Ansätze und Frameworks, welche
MapReduce zum skaliere nutzen [@kolb_parallel_2013,
@malhotra_graph-parallel_2014]. Zudem gibt es immer mehr Bedarf
Vergleichsergebnisse in nahe Echtzeit zu liefern. Erste Ergebnisse Entity
Resolution skalierbar und in nahe Echtzeit zu erreichen, präsentieren Christen &
Gayler in [@christen_towards_2008] 2008, unter Verwendung von Inverted Indexing
Techniken. Dabei betrachten Sie vor allem die Anforderungen eines Anfragestroms
(engl. query stream). Ihre Anforderungen sind einen Strom von Anfragedatesätzen,
gegen potentielle riesige Datenmengen, im Subsekundenbereich pro Anfrage
abzuarbeiten. Dabei sollen die Treffer der Anfrage mit einem Ähnlichkeitswert
versehen sein. Zudem muss es möglich sein die Menge an Anfragen zu skalieren.
Das Hauptproblem ist hierbei die Skalierung. Um skalieren zu können wird
versucht die Abarbeitung des Suchraums zu parallelisieren. Eine Studie von Kwon,
Balazinska, Howe, & Rolia [@kwon_study_2011] in MapReduce Anwendungen zeigt, das
selbst geringe Ungleichgewichte bei der Verteilung des Suchraums auf Mapper bzw.
Reducer, aufgrund der Komplexität der Matching Algorithmen, zu deutlich längeren
Laufzeiten und damit Gesamtlaufzeiten führt. In einem ihrer Beispiele sind bei
einer Gesamtzeit von 5 Minuten die meisten Mapper innerhalb von 30 Sekunden
fertig. Auch beim Streaming kann diese sog. Datenschiefe (engl. data skew) den
Durchsatz eines Clusters signifikant mindern.

# Zielsetzung {#sec:ziele}

Die Personenidentifizierung soll zukünftig schnell, zuverlässig und skalierbar
sein. Personen sollen trotz abweichender Namen, Adressen und Geburtsdaten
möglichst genau identifiziert werden. Bei Abweichungen soll ein Ähnlichkeitswert
(Score) bestimmt werden, der mit Hilfe einer Toleranz für die Identifikation
genutzt werden soll, um Personen zu erkennen. Dazu müssen die Eingabedaten
bereinigt werden. Die Adressbereinigung und Adressvalidierung soll sich auf
Adressen im deutschen Sprachraum konzentrieren. Als Primärziel ist dabei
Deutschland zu betrachten. Die Lösung muss allerdings auch vorsehen andere
Länder mit überschaubarem Aufwand anzubinden. Bei den Namen sollen
Vertauschungen bei Vor- und Nachname, sowie etwaige Titel im Namen erkannt
werden. Die gewählten Algorithmen, die Architektur und das Design sollen in
einem Proof of Concept evaluiert werden. Für das Proof of Concept soll, sofern
möglich auf Open Source Lösungen gesetzt werden.

# Methoden

Zur Umsetzung der in [@sec:ziele] beschriebenen Ziele muss zunächst eine
Wissensbasis durch Literaturarbeit in folgenden Grundlagen geschaffen werden:

* Formate von Adressen im Euroraum
* Charakteristiken von persönlichen Namen
* Möglichkeiten von Eingabefehler persönlicher Daten bei unterschiedlichen
  Medien
* Duplikatserkennung (phonetisch, regelbasierend, …)
* Fehlerkorrektur von Namen und Adressen

Weitere Methoden sind:

* OOP-Entwurf
* Schnittstellen-Entwurf
* Proof of Concept
* Funktionelle Leistungsbewertung anhand realer Anwendungsfälle

# Erwartete Ergebnisse

Die erwarteten Ergebnisse der Masterarbeit sind:

* Analyse der Adressaufbauten im deutschen bzw. europäischen Sprachraum.
* Analyse der Möglichkeiten zur Namensbereinigung
* Analyse der Möglichkeiten zur Adressbereinigung und -validierung
* Analyse der Personenidentifikation anhand bereinigter und validierter
  Adressen
* Design eines Identifikationschecksystems zur Erkennung von Duplikaten
* Prototyp der wesentlichen Funktionen
* Evaluation des Prototypen, anhand der Erwartungen aus der Analyse

# Vorbedingungen

* Adressdatenbank zur Validierung. Kann für Testzwecke aus OpenStreetMap
  extrahiert werden.
* Namensregister zum Abgleich von Vor- und Nachnamen.
* Historie an fehlerhaften und korrigierten Personen- und Adressdaten.

# Literatur
