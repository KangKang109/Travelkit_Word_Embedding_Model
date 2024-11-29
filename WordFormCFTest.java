package com.travelkit.backend.service;
/*
build.gradle파일에 추가

	implementation 'org.apache.commons:commons-text:1.10.0' 

 */
import org.apache.commons.text.similarity.LevenshteinDistance;

public class WordCF2Test {
    public static void main(String[] args) {
        String word1 = "선글라스";
        String word2 = "선글래스";

        // Levenshtein Distance
        LevenshteinDistance levenshtein = new LevenshteinDistance();
        int distance = levenshtein.apply(word1, word2);

        // 결과 출력
        System.out.println("Levenshtein Distance between '" + word1 + "' and '" + word2 + "' is: " + distance);
    }
}
