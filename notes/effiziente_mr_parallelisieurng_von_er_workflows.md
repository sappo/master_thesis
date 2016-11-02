# Effiziente MR Parallelisierung von ER Workflows

Duplikateerkennung ist ein paarweiser Vergleich von Datensätzen bzgl.
verschiedener Ähnlichkeitsmaße. Die Auswertung entspricht dabei dem Kartesischem
Produkt und hat bei n Datensätzen daher eine Komplexität von $O(n^2)$. Zur
Minimierung der Koplexität werden Blocking-, Indexing- oder Windowing-Techniken
genutzt, um den Suchraum einzugrenzen. Dazu werden Datensätz bzgl. einer
Mindesähnlichkeit geclustert.

## ER-Workflow

![ER Workflow](simple_er_workflow.png)

Ein vereinfachter Entity Resolution Workflow ist in Abbildung 1 zu sehen.
Zunächst werden die Datzensätze Vorverarbeitet, um kleinere Fehler zu
korrigieren bzw. Attribute zu vereinheitlichen. Anschließend werden die
Datensätze in Blöcke kategorisiert, wodurch der Suchraum beschränkt wird. Die
Kategorisierung unterliegt der Annahme, dass Duplikate stets in einem Block
landen. Anschließend wird die Ähnlichkeit aller Datensätze eines Blockes
geprüft. Das Ergebnis daraus wird abschließend in *Matches* bzw. *Non-Matches*
klassifiziert.

### Vorverarbeitung

Ziel: Einheitliche Struktur der Datensätze, sowie ein einheitliches Format.

Typische Beispiele:

* Konvertierung von Zahlen und Datumsformaten,
* Korrektur von Tippfehlern
* Ersetzen von Abkürzungen
* Extratction einzelner Bestandteile (z.B. Name-Vorname, Straße-Hausnummer)
* Entfernen von Stoppwörtern, Punkten, Bindestrichen, Kommata,
  aufeinanderfolgende Whitespaces, Anführungszeichen und Satzzeichen
* Konvertierung in Kleinschreibweise

Grund: erhöht die **Robustheit** der Ähnlichkeitsberechnung gegenüber kleineren
Abweichungen. Zudem kann die Ähnlichkeit zweier Zahlen deutlich **effizienter**
bestimmt werden wie bei Zahlenstrings.

### Blocking

Identifikation von Duplikaten erfolgt durch Paarweises vergleichen. Für zwei
Datenquellen A und B sind das $|A|*|B|$ Vergleiche. Bei einer Datenquelle A
$\dfrac{1}{2}*|A|*(|A|-1)$ Vergleiche. In beiden Fällen also quadratisch zu den
Eingabedaten. Zudem sind die Funktionen der Ähnlichkeitsberechnung selbst
rechenintensiv. Auswertung des Kartesischen Produkt ist nachweislich nicht
skalierbar! Zur Effizientssteigerung Einsatz von Blocking-Techniken.

Ziel: der Großteil der *Non-Matches* soll ausgeschlossen werden, ohne dabei
*Matches* auszuschließen. Dadurch wird der Suchraum drastisch reduziert. Übrig
bleibt die sog. Kandidatenpaarmenge.

Effizienz eines Blocking-Algorithmus wird durch *Reduction Ratio*, Reduktion im
Vergleich zum Kartesischen Produkt, und *Pairs Completeness*, Anteil der
tatsächlichen Duplikate, beschrieben.

Für das Blocking werden die Datensätze gruppiert oder sortiert. Dafür werden aus
den Attributen eines Datensatzes *Block-* bzw. *Sortierschlüssel* abgeleitet (=
Signatur des Datensatzes).

#### Standard Blocking

Jedem Datensatz wird ein Blockschlüssel zugewiesen (=konzeptionelle Schlüssel
eines inverted Index). Eine Gruppe von Datensätzen mit selben Blockschlüssel
bilden einen Block. Es werden ausschließlich Datensätze eines Blockes
miteinander verglichen. Anzahl der Vergleiche (=Kandidatenpaare) hängt von der
Größe der Blöcke ab und ist abhängig von der Häufigkeitsverteilung der
Blockschlüsselgenerierung. Ebenso ist die *Pair Completeness* abhängig von der
Blockschlüsselgenerierung. Dem kann mit Multi-pass Blocking entgegengewirkt
werden, d.h. fü einen Datensatz werden mehrere Schlüssel generiert.

#### Q-gram Indexing

Idee: Datensätze mit unterschiedlichen aber ähnlichen Blockschlüsseln
miteinander zu vergleichen.

Ein Blockschlüssel wird dazu in eine Liste von q-Grammen überführt. Ein q-Gram
ist ein Substring der Länge q des ursprünglichen Blockschlüssels.

Nachteil: hoher Aufwand bei der Berechnung aller möglichen Sublisten. Ein
Blockschlüssel mit n Zeichen muss in $k=n-q+1$ q-Gramme zerlegt werden.
Insgesamt müssen $\sum_{i=max\{1,[k*t]\}}^{k} {k \choose i}$ Sublisten
berechnet werden.

#### Suffix Array Indexing

Leitet ähnlich wie Q-gram Indexing auch mehrere Schlüssel aus dem Blockschlüssel
ab. Grundidee ist es alle Suffixe mit einer Mindestlänge von l zu bestimmen. Ein
Datensatz mit Blockschlüssellänge n wird in $n-l+1$ Blöcke eingeordnet. Ist
$n<l$ wird der Ausgangsschlüssel als einziger Schlüssel verwendet.

Nachteil: im Gegensatz zum Standard Blocking ist die Menge an Kandidatenpaaren
deutlich höher. Dadurch ist auch die Wahrscheinlichkeit, dass zwei Datensätze
unnötigerweise mehrfach miteinander verglichen werden hoch.

Vorteil: durch die größere Menge an Kandidatenpaaren ist i.Allg. die *Pair
Completeness* höher. Zudem ist der Aufwand der Berechung der Schlüssel im
Gegensatz zu Q-grammen deutlich geringer.

#### Sorted Neighborhood

Idee: anstatt Datensätze zu partitionieren werden diese anhand eines
Sortierschlüssels geordnet. Dadurch werden ähnliche Datensätze "nah beieinander"
angeordnet. Die Sortierung erfolge durch einen Schlüssel, welcher für jeden
Datensatz generiert wird. Nach der Sortierung aller n Datensätze wird ein
Fenster der Größe $w\in[2,n]$ über die sortierte Liste bewegt. Dabei werden
jeweils alle Datensätze innerhalb des Fensters miteinander verglichen. Insgesamt
git es $n-w+1$ Fensterpositionen und darausfolgend $(n-w/2)*(w-1)$ Vergleiche.
Für die Komplexität bedeutet dies $O(n)+O(n*\log n)+O(n*w)$.

Das Verfahren ist besonders bei der Deduplizierung einer Datenquellen geeignet.
Bei mehreren Datenquellen müssen diese gemischt werden. Dabei besteht die Gefahr
das innerhalb eines Fensters vorrangig Datensätze einer Quelle sind.

Vorteil: Die Anzahl der Kandidatenpaare und damit Vergleiche kann über die
Fenstergröße gesteuert werden.

Nachteil: Anfällig gegen Tippfehler, da zwei Duplikate, deren Blockschlüssel
sich lediglich im ersten Zeichen unterscheidet, nicht erkannt werden.

Eine verbesserte *Pair Completeness* ist durch einen Multi-Pass-Ansatz möglich.
Dabei werden mehrere Sortierschlüssel pro Datensatz generiert.

Problem: Bei beiden Ansätzen gibt es jedoch das Problem, dass die Fenstergröße w
größer als die Anzahl der Datensätze mit dem Sortierschlüssel k sein sollte.
Daher muss für n Datensätze mit Sortierschlüssel k und m Datensätzen mit
Sortierschlüssel k+1 gelten $w=n+m$. Nur dardurch kann sichergestellt werden,
dass der erste Datensatz aus k auch mit allen Datensätzen in k+1 Verglichen
wird. Diese Ausrichtung der Fenstergröße hat jedoch das Problem, das bei selten
auftretenden Sortierschüsseln unnötig oft verglichen wird.

##### Hashtable Verfahren

Idee: für jeden Sortierschlüssel wird die Menge aller Datensätze in eine Liste
gespeichert. Die Sortierschlüssel selbst werden in einer Hashtabelle abgelegt.
Das Fenster wird dann über Hashtabelle geschoben.

Nachteil: Der häufig vorkommenste Schlüssel dominiert die benötigte Zeit zur
Ähnlichkeitsberechnung.

##### Sorted Blocks Verfahren

Idee: zunächst wird wie beim klassischen Verfahren sortiert. Dannach werden
angrenzende Datensätze in disjunkte Partitionen zerlegt. Dabei soll
beispielsweise ein Sortierschlüsselpräfix genuztz werden.

Analog zum Standard Blocking werden alle Datensätze einer Partition miteinander
verglichen. Zusätzlich wird ein Fenster fester Größe über die Partitionsgrenze
geschoben, dabei wird jeweils das erste Element im Fenster mit allen anderen
verglichen. Um zu vermeiden, dass eine Partition dominiert, können größe
Partitionen in Subpartitionen geteilt werden.

##### Adaptive Sorted Neighborhood

Idee: optimale Fenstergröße bestimmen!

Variante 1: Fenster solange vergrößeren bis erster und letzer Datensatz eine
gewisse Mindestähnlichkeit unterschreiten. Nach dem Vergleich aller Datensätze
im Fenster wird dieses zurückgesetzt und an die Position des Datensatzes
geschoben der zum Abbruch der Vergrößerung geführt hat. Diese Variante ist
aufgrund des Aufwandes zur Schlüsselähnlichkeitsberechnung nicht wesentlich
effektiver.

Variante 2: Fenster, beginnend mit $w=2$ solange erhöhen, bis die die Anzahl der
durchschnittlich gefundenen Duplikate pro Vergleich eine Schwelle
unterschreiten.

#### Canopy Clustering

Idee: Datensäzte mittels einfach zu berechnender Abstandsfunktion in
überlappende Cluster partionieren (=Canopies). Datensätze eines Cluster werden
miteinander verglichen.

Zur Generierung wird eine Kandidatenliste gebildet, welche inital als allen
Datensätzen besteht. Dann wird zufällig ein Zentroid eines neuen Clusters
gewählte und alle Datensätze innerhalb des Mindestabstandes $d_1$ zugewiesen.
Zusätzlich werden alle Datensätze dieses Clusters mit einem weiteren
Mindestabstandes $d_2 < d_1$ aus der Kandidatenliste entfernt. Dieser
Algorithmus wird wiederholt, bis die Kandidatenliste leer ist. Die *Pair
Completeness* hängt hierbei stark der gewählten Abstandsfunktion ab.

#### Mapping-basiertes Blocking

Erweiterung des FastMap-Algorithmus. Datensätze werden anhand von
Blockschlüsseln in einen mehrdimensionalen Euklidischen Raum abgebildet, welcher
distanzerhaltend ist. Anschließend ähnlich wie beim Canopy Clustering in
überlappende Partitionen teilen.

Die Art und Weise der Schlüsselgenerierung hat entscheidenden Einfluss auf die
Qualität der ER-Workflows. Ist das Blocking-Kriterium zu "scharf", werden
Duplikate nicht gefunden, ist es zu "lax", sind die resultierenden Cluster sehr
groß und die Anzahl der Vergleiche steigt drastisch.

Zum Aufstellen von Regeln zur Generierung gibt es zwei Möglichkeite:

* Domänenexperten
* Maschine-Learning Verfahren

### Ähnlichkeitsberechnung

Zur Berechnung der Ähnlichkeit zweier Datensätze, werden i.Allg. mehrere
Ähnlichkeitsfunktionen auf die Attributewerte der Datensätze angewandt. Statt
Ähnlichkeiten können auch Abstandsmaße genutzt werden, welche in eine
Ähnlichkeit umgewandelt werden müssen.

**Field Matching** beschreibt die Berechnung der Ähnlichkeit einzig anhander
deren Attributewerte. Dies wird v.a. durch Zeichenkettenähnlichkeitsmaße
durchgeführt. Alternative werden Tokenbasierte Maße genutzt. Hierbei wird die
Zeichenkette in Token zerlegt und anschließend die Ähnlichkeit der Tokenmengen
ermittelt. Verschiedene Maße eignen sich unterschiedlich für bestimmte
Attributetypen. Da dies selbst für Domainexperten schwierig herauszufinden ist,
werden oft Maschine-Learning Verfahren genutzt, um ein passendes Maß für ein
Attributstyp zu finden.

**Kontexbasierte Verfahren** nutzen zur Bestimmung der Ähnlichkeit assozierte
Datenen. Im einfachsten Fall, werden diese einfach an die Datensätze angehängt.
Weiter Beispiele sind XML, durch Ausnutzung der Struktur, Graphen, wo
Assoziationen durch Kanten dargestellt werden, oder ontologische Strukturen,
beispeilsweise OWL.

### Klassifizierung

Bestimmung der tatsächlichen Duplikate auf Basis von Ähnlichkeitsvektoren.

**Wahrscheinlichkeitsbasierte Verfahren** beispeilsweise Bayes. Nicht mehr State
of the Art.

**Schwellwertbasierte Verfahren** aggregieren die Komponenten eines
Ähnlichkeitsvektors, mittels einer einfachen oder gewichteten Summe. Ein
Schwellwert wird genutzt, um Matches von Not-Matches zu unterscheiden. Eine
erweiterte Form nutzt zwei Schwellwerte zur Unterscheidung von sicheren Matches
und wahrscheinlichen, welche manuell überprüft werden müssen.

**Regelbasierte Verfahren** treffen Entscheidungen anhand von Matching-Regeln in
konjunktiver oder disjunktiver Normalform. Die Aufstellung der Regeln erfolgt
durch Domänenexperten und ist ein aufwändiger, iterativer Prozess. Zusätzlich
können Contraints genutzt werden, um domänspezifische Integritätsbedingungen
sicherzustellen.

**Maschienelle Lernverfahren** sind vorrangig überwachte Lernverfahren, die auf
Basis der Ähnlichkeitsvektoren manuell gelabelter Trainingsdaten ein
Klassifikationsmodell generieren, welches anschließend auf ungelabelte
Ähnlichkeitsvektoren angewandt wird. Populäre Klassifikatoren sind:

* Entscheidungsbäume und
* Support Vector Maschines (SVM)

Die Qualität dieser Verfahren hängt von der Menge und Aussagekraft der manuellen
Trainingsdaten ab. Zusätztlich können verschiedene Verfahren kombiniert werden,
die unabhängig voneinander trainiert worden sind.

**Active Learning** sind Verfahren die mit wesentlich weniger Trainingsdaten
auskommen und kaum manuellen Aufwand benötigen. Hierbei wird ein initales
Klassifikationsmodell aus einer kleinen Menge an Trainingsdaten erstellt,
welches iterativ durch Nutzerfeedback verfeinert wird. Dabei müssen die
Kandidatenpaare, die am schwierigsten zu klassifizieren waren manuell
Klassifiziert werden.

### Nachverarbeitung

Berechnung der transitiven Hülle zur Beseitigung von Kontradiktionen der Menge
der klassifizierten Duplikate und Nicht-Duplikate. Dazu ist ein sog. perfektes
Match-Ergebnis erforderlicht, auch Gold Standard gennant. Dadurch iest es
möglich die True Positives, False Positives, True Negatives und False Negatives
zu ermitteln. Daraus werden dann die Kennzahlen *Precision*, *Recall* und
*F-Measure* (harmonisches Mittel) abgeleitet.

## MapReduce Erweiterungen

**Lastbalancierung** ohne Lastbalancierung stellt die Bearbeitung des größten
Block, die untere Schranke der Bearbeitungszeit dar.

**Speicherengpässe** zum Vergleich eines Blocks müssen alle Datensätze im
Hauptspeicher gehalten werden. Unter Berücksichtigung aller Prozesse muss die
maximale Blockgröße bestimmt und eingehalten werden.

**Redundante Ähnlichkeitsbestimmung** entsteht durch Multi-Pass-Blocking
Verfahren oder Verfahren mit überlappenden Clustern.

**Integration maschineller Lernverfahren** beim Clustering, bei der Auswahl der
Ähnlichkeitsfunktion für einen Attributswert und bei der Klassifizierung in
Matches und Non-Matches.

**Iterative Berechung der transitiven Hülle** zum Evaluieren des Matching
Ergebnisses gegenüber dem Gold Standard.
