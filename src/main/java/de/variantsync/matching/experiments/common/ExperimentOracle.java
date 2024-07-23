package de.variantsync.matching.experiments.common;

import de.variantsync.matching.raqun.data.RElement;
import de.variantsync.matching.raqun.data.RMatch;

import java.util.*;

/**
 * Utility class for calculating precision, recall and f-measure
 */
public class ExperimentOracle {

    private double tp;
    private double fp;
    private double fn;
    private double precision;
    private double recall;
    private double fMeasure;

    /**
     * Initialize a new oracle with the provided matches and calculate the statistics.
     * @param matches The matches calculated by a matcher
     */
    public ExperimentOracle(final Set<RMatch> matches) {
        calculate(matches);
    }

    private void calculate(final Set<RMatch> matches) {
        tp = 0.0;
        fp = 0.0;
        fn = 0.0;
        final Map<String, Integer> numberOfClassOccurrencesTotal = countClassOccurrences(matches);

        for (final RMatch match : matches) {
            final Collection<RElement> elements = match.getElements();
            // Count the number of times each class appears in the tuple
            final Map<String, Integer> numberOfClassOccurrences = new HashMap<>();
            for (final RElement elem : elements) {
                final String id = elem.getUUID();
                if (numberOfClassOccurrences.containsKey(id)) {
                    final int oldNumber = numberOfClassOccurrences.get(id);
                    numberOfClassOccurrences.put(id, oldNumber+1);
                } else {
                    numberOfClassOccurrences.put(id, 1);
                }
            }

            // Now we count the number of TP, FP, FN for the current tuple
            for (final String id : numberOfClassOccurrences.keySet()) {
                final int numberCurrent = numberOfClassOccurrences.get(id);
                final int numberOther = elements.size() - numberCurrent;

                // Count the tp, one for each correct match between members of a class
                for (int i = numberCurrent-1; i > 0; i--) {
                    tp += i;
                }

                // Count the fp, one for each incorrect match between members of different classes
                fp += numberCurrent * numberOther;

                // Count the fn, one for each missing match with a member of the current class
                final int numberMissing = numberOfClassOccurrencesTotal.get(id) - numberCurrent;
                fn += numberCurrent * numberMissing;
                // We have to set the new value so that every missing match is only counted once
                numberOfClassOccurrencesTotal.put(id, numberMissing);
            }
        }
        // We have to halve the number of fp, because we counted them twice
        fp /= 2;
    }

    private void calculateStats() {
        if (tp == 0) {
            precision = 0.0d;
            recall = 0.0d;
            fMeasure = 0.0d;
        } else {
            precision = tp / (tp + fp);
            recall = tp / (tp + fn);
            fMeasure = (2 * (precision * recall)) / (precision + recall);
        }
    }

    public double getTp() {
        return tp;
    }

    public double getFp() {
        return fp;
    }

    public double getFn() {
        return fn;
    }

    public double getPrecision() {
        return precision;
    }

    public double getRecall() {
        return recall;
    }

    public double getFMeasure() {
        return fMeasure;
    }

    private Map<String, Integer> countClassOccurrences(final Set<RMatch> mergedModel) {
        final Map<String, Integer> numberOfClassOccurrences = new HashMap<>();

        for (final RMatch tuple : mergedModel) {
            countClassOccurrencesInTuple(tuple, numberOfClassOccurrences);
        }
        return numberOfClassOccurrences;
    }

    private void countClassOccurrencesInTuple(final RMatch tuple, final Map<String, Integer> classOccurrences) {
        // Counts the number of times each class appears in the given tuple and updates the given map that holds previous
        // counts of class occurrences
        for (final RElement node : tuple.getElements()) {
            final String id = node.getUUID();
            if (classOccurrences.containsKey(id)) {
                final Integer count = classOccurrences.get(id) ;
                classOccurrences.put(id, count + 1);
            } else {
                classOccurrences.put(id, 1);
            }
        }
    }


}