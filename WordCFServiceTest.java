package com.travelkit.backend.service;

import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.embeddings.wordvectors.WordVectors;

import java.io.File;
import java.util.List;
import java.util.ArrayList;

public class WordCFServiceTest {
    public static void main(String[] args) {
        try {
            // 모델 파일 경로 설정 (gensim에서 텍스트 형식으로 저장한 경로)
            String modelPath = "C:\\Users\\minwo\\Documents\\word2vec\\word2vec_model_koreanB62M.txt";  // 실제 경로로 변경

            // 모델 로드
            File modelFile = new File(modelPath);
            WordVectors wordVectors = WordVectorSerializer.loadStaticModel(modelFile);

            // 유사도 계산할 단어 리스트
            String[] wordsToTest = {"후드티", ""};

            // 모든 단어 간의 유사도 계산
            for (int i = 0; i < wordsToTest.length; i++) {
                for (int j = i + 1; j < wordsToTest.length; j++) {
                    String word1 = wordsToTest[i];
                    String word2 = wordsToTest[j];

                    // 유사도 계산
                    if (wordVectors.hasWord(word1) && wordVectors.hasWord(word2)) {
                        double similarity = wordVectors.similarity(word1, word2);
                        System.out.println(word1 + "와 " + word2 + "의 유사도: " + similarity);
                    } else {
                        System.out.println("단어가 모델에 없습니다: " + word1 + " 또는 " + word2);
                    }
                }
            }

        } catch (Exception e) {
            System.out.println("오류 발생: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
