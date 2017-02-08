# Annotierte Gliederung

1. Einleitung

2. Grundlagen / Related works
    * Entity Resolution
        - Was ist die Disziplin? Woher kommt Sie?
        - Welcher Schritte sind involviert?
            ~ Vorverarbeitung
            ~ Blocken
            ~ Lernen
            ~ Klassifizieren
    * Statisches Blocking
        - Beliebteste Methoden von Standard Blocking bis Sorted Neighborhood
    * Dynamisches Blocking
        - DySimII (Simlarity Aware Index)
        - LSI (Simlarity Aware Index with LSH)
        - DySNI (Simlarity Aware Sorted Neighborhood)
        - Pay as you go! (Erhalte Ergebnisse welche in n Zeit berechnet wurde)
    * Ähnlichkeitsmaße
    * Klassifizierer

3. Analyse
    * DySimII/LSI
        - Was funtioniert?
        - Wo liegen die Schwierigkeiten?
            ~ Kandidatenmenge
            ~ Parametervielfalt
            ~ Blocking Schema
    * Schwache Labels
        - Generieren von Groud Truth
            ~ Mit Ground Truth - nur negative
            ~ Ohne Ground Truth - negative und positive
            ~ Übertragbarkeit von Schranken auf andere Datensätze
            ~ Auswählen über Wahrscheinlichkeitsverteilung!
    * Ähnlichkeitsmaße
        - Welche funktionieren auf welchen Daten?
        - Wie können Parameter der Funktionen zum Optimieren genutzt werden?
        - Wie wählt man sinnvoll Ähnlichkeitsmaße aus?
    * Blocking-Schema
        - A. und O. bei Entity Resolution, aber schwierig zu definieren
        - Wie kann man das automatisieren?
        - DNF-Blocking Schema
        - Scoring der Blockschlüssel
            ~ Funktionen, Parameter, Gewichtung, Normalisierung?
    * Modifiziertes Blocking/Indexing
        - MDySimII -> Was funtioniert hier nicht
        - MDySimIII - Verbesserungen
        - MDyLSH
    * Klassifizierer
        - Datenaufbereitung für Klassifizierer
        - Welche kommen in Frage?

4. Design
    * SimIndex
        - Bestandteile erklären, durch Analyse bekräftigen
            ~ Vorverarbeitung
            ~ WeakLabels
            ~ Blocking-Schema
            ~ Similarities
            ~ Blocking (MDySimIII, MDyLSH)

5. Umsetzung

6. Evaluation (Gesamtsystem)
    * Verschiedene Dataset gegen Baseline testen
    * Auswirking der Gewichte beim DNF-Schema
    * Auswirkung der Ähnlichkeitsmaße

7. Fazit/Ausblick
