---
# Expose Masterarbeit

author: Kevin Sapper
title: Skalierbares Echtzeit Entity Resolution Streaming Framework (Working Titel)
referent: Prof. Dr. Reinhold Kröger
coreferent: Prof. Dr. Adrian Ulges
handler: Thomas Strauß (Universum Group)
company: Detim Consulting GmbH / Universum Group

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
die Entitäten nicht durch ein einzigartiges Attribute identifiziert werden.
Zudem sind die Datensätze oft fehlerhaft, beispielsweise durch
Rechtschreibfehler oder unterschiedliche Konventionen. Die Methoden zur
Entitätsauflösung arbeiten meist auf Datensatzpaaren und liefern als Ergebnis
einen Ähnlichkeitswert (engl. similarity score). Über den Ähnlichkeitswert kann
bestimmt werden, ob ein Datensatzpaare übereinstimmt (engl. match) oder nicht.

Zur Bestimmung der Ähnlichkeit eines Datensatzpaares unterscheiden Elmagarmid et
al. [@elmagarmid_duplicate_2007] zwischen Attributevergleichs- (engl. field
matching) und Datensatzvergleichsmethoden (engl. detecting duplicate records).
Methoden zum Attributevergleich sind zeichenbasierend (edit distance, affine gap
distance, Jaro distance metric oder Q-gram distance), tokenbasierend (atomic
strings, Q-grams mit tf.idf), phonetisch (soundex) oder nummerisch. Die
Datensatzvergleichsmethoden sind probabilistisch (Naive Bayes), überwachtes bzw.
semi-überwachtes Lernen (Support Vector Maschine, Markov Chain Monte Carlo),
aktives Lernen (ALIAS), distanzebasierend (siehe Attributevergleich - Datensatz
als konkatenierter String) oder regelbasierend (AJAX).

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
* Namesregister zum Abgleich von Vor- und Nachnamen.
* Historie an fehlerhaften und korrigierten Personen- und Adressdaten.

# Literatur
